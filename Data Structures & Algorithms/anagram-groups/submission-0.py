class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        storeMap = {} # value: [str, str, str ...]
        for string in strs:
            sorted_string = ''.join(sorted(string))
            if sorted_string not in storeMap:
                storeMap[sorted_string] = []
            storeMap[sorted_string].append(string) 
        return list(storeMap.values())