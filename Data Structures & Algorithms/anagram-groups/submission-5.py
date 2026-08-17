class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if strs == [""]:
            return [[""]]

        sorted_map = defaultdict(list) # sorted_val: [strs]

        for each_str in strs:
            sorted_value = ''.join(sorted(each_str))
            sorted_map[sorted_value].append(each_str)
        return list(sorted_map.values())