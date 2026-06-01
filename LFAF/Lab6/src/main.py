"""
Entry point — demonstrates the lexer, parser, and AST pretty-printer.
"""

from Lexer  import tokenize
from Parser  import Parser


def print_ast(node, indent=0):
    """Recursively pretty-print an AST with indentation."""
    pad = "  " * indent
    from ast_nodes import NumberNode, BinOpNode, UnaryOpNode

    if isinstance(node, NumberNode):
        print(f"{pad}Number({node.value})")

    elif isinstance(node, BinOpNode):
        print(f"{pad}BinOp({node.op.value!r})")
        print_ast(node.left,  indent + 1)
        print_ast(node.right, indent + 1)

    elif isinstance(node, UnaryOpNode):
        print(f"{pad}UnaryOp({node.op.value!r})")
        print_ast(node.operand, indent + 1)


def run(expression):
    print(f"\n{'='*50}")
    print(f"  Input: {expression}")
    print(f"{'='*50}")

    # --- Lexing ---
    tokens = tokenize(expression)
    print("\n[Tokens]")
    for tok in tokens:
        print(f"  {tok}")

    # --- Parsing ---
    parser = Parser(tokens)
    ast    = parser.parse()

    # --- AST ---
    print("\n[AST]")
    print_ast(ast)


if __name__ == '__main__':
    expressions = [
        "3 + 5",
        "10 - 2 * 3",
        "(1 + 2) * (3 + 4)",
        "2 ^ 3 ^ 2",          # right-associative: 2^(3^2) = 2^9
        "-5 + 3",
        "3.14 * (2 + 1)",
    ]
    for expr in expressions:
        run(expr)