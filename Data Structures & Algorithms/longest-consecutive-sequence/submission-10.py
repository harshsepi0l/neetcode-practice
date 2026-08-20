class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if nums == []:
            return 0
        n = sorted(set(nums))
        count = 1
        longest = 1
        for i in range(len(n) - 1):
            if n[i + 1] - n[i] == 1:
                count += 1
                longest = max(longest, count)
            else:
                count = 1
        return longest