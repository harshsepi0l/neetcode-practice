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

                # Truncate toward zero without using float division
                num = abs(left) // abs(right)
                if (left < 0) != (right < 0):
                    num = -num

                stack.pop()
                stack.pop()
                stack.append(num)

            else:
                stack.append(int(e))

        return stack[0]