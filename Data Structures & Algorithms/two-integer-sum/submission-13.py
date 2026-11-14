class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # enumerate to keep track of the indices and then check if the difference is in the list and get the index
        
        seen = defaultdict(int)
        for i, n in enumerate(nums):
            diff = target - n
            if diff in seen:
                return [seen[diff], i]
            seen[n] = i