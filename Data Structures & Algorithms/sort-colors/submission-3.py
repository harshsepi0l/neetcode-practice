class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        
        count = [0] * 3
        
        for i in range(len(nums)):
            count[nums[i]] += 1
        # count -> [1, 2, 1]

        j = 0
        for i in range(len(count)):
            while count[i] != 0:
                nums[j] = i
                count[i] -= 1
                j += 1

        
        