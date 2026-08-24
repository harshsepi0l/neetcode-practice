class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if strs == [""]:
            return [[""]]

        sorted_map = defaultdict(list)

        for s in strs:
            sorted_val = ''.join(sorted(s))
            sorted_map[sorted_val].append(s)

        return list(sorted_map.values())