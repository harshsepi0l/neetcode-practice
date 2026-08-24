class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        par_map = {")" : "(", "]" : "[", "}" : "{"}

        for char in s:
            if char in par_map:
                if stack and stack[-1] == par_map[char]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(char)
        
        return True if not stack else False