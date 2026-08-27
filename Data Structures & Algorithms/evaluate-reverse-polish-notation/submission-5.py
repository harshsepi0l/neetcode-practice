class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        for t in tokens:
            if t == '+':
                j = len(stack) - 1
                num = int(stack[j - 1]) + int(stack[j]) 
                stack.pop()
                stack.pop()
                stack.append(num)
            elif t == '-':
                j = len(stack) - 1
                num = int(stack[j - 1]) - int(stack[j]) 
                stack.pop()
                stack.pop()
                stack.append(num)
            elif t == '*':
                j = len(stack) - 1
                num = int(stack[j - 1]) * int(stack[j]) 
                stack.pop()
                stack.pop()
                stack.append(num)
            elif t == '/':
                j = len(stack) - 1
                num = int(int(stack[j - 1]) / int(stack[j]))
                stack.pop()
                stack.pop()
                stack.append(num)
            else:
                stack.append(int(t))
        return stack[0]