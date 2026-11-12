class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        # two hashmaps that are set to a value s_map = {r: 2, a: 2...} t_map = {r: 2, a: 2}

        s_map = defaultdict(int)
        t_map = defaultdict(int)

        for i in range(len(s)):
            s_map[s[i]] = 1 + s_map[s[i]]
            t_map[t[i]] = 1 + t_map[t[i]]

        return s_map == t_map
