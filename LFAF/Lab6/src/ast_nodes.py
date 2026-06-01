"""
AST node definitions.
Each node type represents one syntactic construct in an arithmetic expression.
"""


class NumberNode:
    """Leaf node — a numeric literal."""
    def __init__(self, value):
        self.value = float(value)

    def __repr__(self):
        return f"Number({self.value})"


class BinOpNode:
    """Binary operation: left OP right."""
    def __init__(self, left, op, right):
        self.left  = left
        self.op    = op      # Token (PLUS / MINUS / MUL / DIV / POWER)
        self.right = right

    def __repr__(self):
        return f"BinOp({self.left!r}, {self.op.value!r}, {self.right!r})"


class UnaryOpNode:
    """Unary operation: OP operand  (e.g. negation)."""
    def __init__(self, op, operand):
        self.op      = op
        self.operand = operand

    def __repr__(self):
        return f"UnaryOp({self.op.value!r}, {self.operand!r})"