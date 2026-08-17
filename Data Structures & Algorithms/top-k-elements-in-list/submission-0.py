class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        
        count = defaultdict(int) # val:count
        freq = [[] for i in range(len(nums)+1)]
        for num in nums:
            count[num] += 1    
        for num, cnt in count.items():
            freq[cnt].append(num)
        
        k_res = []
        for i in range(len(freq)-1, 0, -1):
            for num in freq[i]:
                k_res.append(num)
                if len(k_res) == k:
                    return k_res