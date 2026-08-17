class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # map to hashmap then compare the results

        if len(s) != len(t):
            return False
        
        sMap = {} # value: count
        tMap = {} # value: count

        for i in range(len(s)):
            sMap[s[i]] = 1 + sMap.get(s[i], 0)
            tMap[t[i]] = 1 + tMap.get(t[i], 0)

        return sMap == tMap