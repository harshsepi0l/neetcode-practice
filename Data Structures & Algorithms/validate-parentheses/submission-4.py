class Solution:
    def isValid(self, s: str) -> bool:
        # map the closing brack to the opening brack and check if the appended item in the 
        # stack and the last item in the stack equals the key:value pairs

        close_to_open = { ')': '(', ']' : '[', '}' : '{'} # close : open
        stack = []
        
        # 1) check if the char is in close_to_open
        for char in s:
            if char in close_to_open:
                # 2) check if stack and stack[-1] == close_to_open[char] <-- should be appended
                if stack and stack[-1] == close_to_open[char]:
                    # we pop the stack if those are equal to the char
                    stack.pop()
                else:
                    return False
            else:
                stack.append(char)

        # 4) only return true if the stack is empty

        return True if not stack else False