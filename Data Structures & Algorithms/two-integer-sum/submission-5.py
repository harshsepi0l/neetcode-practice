class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # 7 - 4 = 3 which exists
        # use a hashmap to remember the prev values and indices
        # prevMap -> val: index
        # then if that difference exists thats the answer

        prevMap = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in prevMap:
                return [prevMap[diff], i]
            prevMap[num] = i