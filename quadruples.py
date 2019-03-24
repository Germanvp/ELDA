def push(stack, value):
    """
    Adds a member to the specified stack.
    :param stack: The stack to add to
    :param value: The value to add
    """
    stack.append(value)


def pop(stack):
    """
    Pops a member from the specified stack.
    :param stack: The stack to pop from
    :return: The popped value
    """
    return stack.pop()


class Quadruples:
    """
    Handles quadruple generation and stacks.
    """

    def __init__(self):
        self.operand_stack = []
        self.operator_stack = []
        self.type_stack = []
