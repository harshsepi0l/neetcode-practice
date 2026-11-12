#!/usr/bin/env python3
"""Fill in "Done on" in the Notion Problem Log from NeetCode submission commits.

NeetCode's GitHub Sync commits each submission as
    Data Structures & Algorithms/<neetcode-id>/submission-N.<ext>

This script walks the git history from START_DATE on, takes the first commit
date for each problem folder, matches the folder to a Problem Log row by the
LeetCode slug in the row's Link, and sets Done on when it's still empty.

It never touches First try, Clue, Needs redo or any other field, never
overwrites a Done on that's already set, and never creates rows. Folders it
can't match are printed as warnings.

Env vars:
    NOTION_TOKEN            Notion internal integration secret (required unless --dry-run with --offline)
    NOTION_DATA_SOURCE_ID   Problem Log data source id (required unless --offline)
    START_DATE              Only commits on or after this date count (default 2026-11-12)
    TZ_NAME                 Time zone for commit dates (default America/Detroit)

Stdlib only, so the workflow needs no pip install.
"""

import argparse
import difflib
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"
DSA_DIR = "Data Structures & Algorithms"
SLUG_RE = re.compile(r"(?:leetcode\.com|neetcode\.io)/problems/([^/?#]+)")

PROP_TITLE = "Problem"
PROP_LINK = "Link"
PROP_DONE = "Done on"

HERE = os.path.dirname(os.path.abspath(__file__))


def warn(msg):
    # GitHub Actions turns this into a yellow annotation on the run
    if os.environ.get("GITHUB_ACTIONS"):
        print(f"::warning::{msg}")
    else:
        print(f"WARNING: {msg}")


# ---------- git side ----------

def first_submission_dates(repo, start_date, tz_name):
    """Return {neetcode_id: 'YYYY-MM-DD'} with the earliest commit date on/after start_date."""
    env = dict(os.environ, TZ=tz_name)
    out = subprocess.run(
        [
            "git", "-C", repo, "log", "--reverse",
            "--diff-filter=AM", "--name-only",
            "--date=format-local:%Y-%m-%d",
            "--format=@@%cd",
            f"--since={start_date} 00:00",
            "--", DSA_DIR,
        ],
        env=env, check=True, capture_output=True, text=True,
    ).stdout

    first = {}
    current = None
    for line in out.splitlines():
        if line.startswith("@@"):
            current = line[2:]
            continue
        parts = line.split("/")
        if current is None or len(parts) < 3 or parts[0] != DSA_DIR:
            continue
        # --since filters on commit time in the runner's view; re-check the local date
        if current < start_date:
            continue
        pid = parts[1]
        if pid not in first or current < first[pid]:
            first[pid] = current
    return first


# ---------- Notion side ----------

def notion(method, path, token, body=None, retries=4):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        f"{NOTION_API}{path}", data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_VERSION,
            "Content-Type": "application/json",
        },
    )
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries:
                time.sleep(float(e.headers.get("Retry-After", 2 ** attempt)))
                continue
            detail = e.read().decode(errors="replace")
            sys.exit(f"Notion API {method} {path} failed ({e.code}): {detail}")


def plain_text(prop):
    if not prop:
        return ""
    kind = prop.get("type")
    if kind == "url":
        return prop.get("url") or ""
    if kind in ("title", "rich_text"):
        return "".join(t.get("plain_text", "") for t in prop.get(kind, []))
    return ""


def load_rows(token, data_source_id):
    """Return list of {id, title, slug, done} for every Problem Log row."""
    rows, cursor = [], None
    while True:
        body = {"page_size": 100}
        if cursor:
            body["start_cursor"] = cursor
        res = notion("POST", f"/data_sources/{data_source_id}/query", token, body)
        for page in res["results"]:
            props = page["properties"]
            link = plain_text(props.get(PROP_LINK))
            m = SLUG_RE.search(link)
            done = (props.get(PROP_DONE) or {}).get("date")
            rows.append({
                "id": page["id"],
                "title": plain_text(props.get(PROP_TITLE)),
                "slug": m.group(1).lower() if m else None,
                "done": done.get("start") if done else None,
            })
        if not res.get("has_more"):
            return rows
        cursor = res["next_cursor"]


def set_done_on(token, page_id, date):
    notion("PATCH", f"/pages/{page_id}", token,
           {"properties": {PROP_DONE: {"date": {"start": date}}}})


# ---------- matching ----------

def load_aliases(path):
    with open(path) as f:
        data = json.load(f)
    return {k.lower(): v.lower() for k, v in data.items() if not k.startswith("_")}


def match(first_dates, rows, aliases):
    """Return (matches, unmatched). matches: list of (neetcode_id, date, row)."""
    by_slug = {}
    for r in rows:
        if r["slug"]:
            by_slug.setdefault(r["slug"], r)
    matches, unmatched = [], []
    for pid, date in sorted(first_dates.items(), key=lambda kv: kv[1]):
        # neetcode.io links use the folder name as-is; leetcode.com links may need an alias
        slug = aliases.get(pid.lower(), pid.lower())
        row = by_slug.get(pid.lower()) or by_slug.get(slug)
        if row:
            matches.append((pid, date, row))
        else:
            guess = difflib.get_close_matches(slug, by_slug.keys(), n=1, cutoff=0.6)
            unmatched.append((pid, date, guess[0] if guess else None))
    return matches, unmatched


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=".", help="path to the neetcode-practice checkout")
    ap.add_argument("--dry-run", action="store_true", help="print what would change, write nothing")
    ap.add_argument("--rows-json", help="offline test: read rows from this JSON file instead of Notion")
    ap.add_argument("--aliases", default=os.path.join(HERE, "neetcode_aliases.json"))
    args = ap.parse_args()

    start = os.environ.get("START_DATE", "2026-11-12")
    tz_name = os.environ.get("TZ_NAME", "America/Detroit")
    token = os.environ.get("NOTION_TOKEN", "")
    ds_id = os.environ.get("NOTION_DATA_SOURCE_ID", "")

    first = first_submission_dates(args.repo, start, tz_name)
    print(f"Problems with a submission on or after {start}: {len(first)}")
    if not first:
        return

    if args.rows_json:
        with open(args.rows_json) as f:
            rows = json.load(f)
    else:
        if not token or not ds_id:
            sys.exit("Set NOTION_TOKEN and NOTION_DATA_SOURCE_ID.")
        rows = load_rows(token, ds_id)
    print(f"Problem Log rows: {len(rows)}")

    matches, unmatched = match(first, rows, load_aliases(args.aliases))

    updated = skipped = 0
    for pid, date, row in matches:
        if row["done"]:
            skipped += 1
            print(f"  keep   {row['title']}: Done on already {row['done']}")
            continue
        print(f"  {'would set' if args.dry_run else 'set'}  {row['title']}: Done on {date}  (from {pid})")
        if not args.dry_run:
            set_done_on(token, row["id"], date)
            time.sleep(0.35)  # stay under Notion's ~3 requests/second
        updated += 1

    for pid, date, guess in unmatched:
        hint = f" Closest row slug: {guess}. Add \"{pid}\": \"{guess}\" to neetcode_aliases.json if that's it." if guess else ""
        warn(f"No Problem Log row for folder '{pid}' (first submitted {date}).{hint}")

    verb = "Would update" if args.dry_run else "Updated"
    print(f"{verb} {updated}, left {skipped} that already had a date, {len(unmatched)} unmatched.")


if __name__ == "__main__":
    main()
