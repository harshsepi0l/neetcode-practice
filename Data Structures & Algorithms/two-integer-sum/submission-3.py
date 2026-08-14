class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        map_num = {}
 
        for i, n in enumerate(nums):
            diff = target - n
            if diff in map_num:
                return [map_num[diff], i]
            map_num[n] = i