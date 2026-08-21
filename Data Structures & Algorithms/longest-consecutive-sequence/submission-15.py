class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        
        nums_set = set(nums)
        longest = 0
        length = 0

        for n in nums_set:
            # check if n has a left neighbor
            if (n - 1) not in nums_set:
                # find all numbers where n + 1 is in the set
                 while (n + length) in nums_set:
                    length += 1
                    longest = max(longest, length)
            length = 0
        
        return longest