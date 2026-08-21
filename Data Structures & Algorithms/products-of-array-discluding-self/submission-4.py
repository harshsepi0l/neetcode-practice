class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [1] * n 
        # first calculate the prefix
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]
        # 1, 1, 2, 8 | prefix = 48
        # now calculate the postfix (decrement from the loop from the last integer)
        postfix = 1
        for i in range(n-1, -1, -1):
            res[i] *= postfix
            postfix *= nums[i]
        
        return res
            
