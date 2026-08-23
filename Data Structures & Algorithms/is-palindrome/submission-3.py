class Solution:
    def isPalindrome(self, s: str) -> bool:
        letters = [char.lower() for char in s if char.isalnum()]

        
        L = 0
        R = len(letters) - 1

        while L < R:
            if letters[L] != letters[R]:
                return False
            L+=1
            R-=1
        return True