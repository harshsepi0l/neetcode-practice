class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        sortedMap = defaultdict(list) #sorted val: [strs]
        for s in strs:
            sortedS = ''.join(sorted(s))
            sortedMap[sortedS].append(s)
        
        return list(sortedMap.values())

        