class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        
        count = defaultdict(int)

        for i in range(len(nums)):
            prev = target - nums[i]
            if prev in count:
                return [count[prev], i]

            count[nums[i]] = i