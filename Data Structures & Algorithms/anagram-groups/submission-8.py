class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # act: act, cat
        # opst: stop, pots, tops
        # aht: hat

        count_s = defaultdict(list)
        for string in strs:
            sorted_str = " ".join(sorted(string))
            count_s[sorted_str].append(string)
        return list(count_s.values())