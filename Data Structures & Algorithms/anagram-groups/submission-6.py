class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        # sort the values and then use a hashmap to map the sorted value to the values

        sort_map = defaultdict(list)

        for each_str in strs:
            sorted_val = ''.join(sorted(each_str))
            sort_map[sorted_val].append(each_str)
        
        return list(sort_map.values())