class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []

        for e in tokens:
            if e == "+":
                j = len(stack) - 1
                num = stack[j - 1] + stack[j]
                stack.pop()
                stack.pop()
                stack.append(num)

            elif e == "-":
                j = len(stack) - 1
                num = stack[j - 1] - stack[j]
                stack.pop()
                stack.pop()
                stack.append(num)

            elif e == "*":
                j = len(stack) - 1
                num = stack[j - 1] * stack[j]
                stack.pop()
                stack.pop()
                stack.append(num)

            elif e == "/":
                j = len(stack) - 1
                left = stack[j - 1]
                right = stack[j]
                num = int(float(left) / right)
                stack.pop()
                stack.pop()
                stack.append(num)

            else:
                stack.append(int(e))

        return stack[0]