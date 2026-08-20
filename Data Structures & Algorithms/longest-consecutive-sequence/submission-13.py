class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for n in num_set:
            # check if the sequence exists (check if it has a left neighbor)
            if (n - 1) not in num_set:
                length = 0
                while (n + length) in num_set:
                    length += 1
                
                longest = max(longest, length)

        return longest
                