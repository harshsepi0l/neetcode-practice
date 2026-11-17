class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        s_map = defaultdict(list)
        for s in strs:
            sorted_s = ''.join(sorted(s))
            s_map[sorted_s].append(s)
            
        return list(s_map.values())