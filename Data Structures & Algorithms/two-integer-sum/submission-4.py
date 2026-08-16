class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        countMap = defaultdict(list) # val: index
        for i, n in enumerate(nums):
            diff = target - n
            if diff in countMap:
                return [countMap[diff], i]
            countMap[n] = i
            



            