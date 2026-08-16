class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        if strs == [""]:
            return [[""]]
        
        sort_map = defaultdict(list)
        for each_str in strs:
            sorted_str = ''.join(sorted(each_str))
            sort_map[sorted_str].append(each_str)
        
        return list(sort_map.values())

