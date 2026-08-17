class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # create an arr with all occurences (count)
        # then use the count of occurrences to replace 
        # values in the og array
        # can be done using bucket sort

        count = [0] * 3

        for num in nums:
            count[num]+=1
        #1,2,1

        index = 0
        for i in range(len(count)):
            while count[i]:
                count[i]-=1
                nums[index] = i
                index+=1