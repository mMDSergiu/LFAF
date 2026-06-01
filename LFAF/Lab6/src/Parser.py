"""
Recursive-descent parser for arithmetic expressions.

Grammar (in order of increasing precedence):
    expr     → term   (('+' | '-') term)*
    term     → factor (('*' | '/') factor)*
    factor   → base   ('^' factor)*        # right-associative
    base     → NUMBER
             | '(' expr ')'
             | ('+' | '-') base            # unary +/-
"""

from Lexer    import TokenType
from ast_nodes import BinOpNode, UnaryOpNode, NumberNode


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos    = 0

    # --- helpers -----------------------------------------------------------

    def _current(self):
        return self.tokens[self.pos]

    def _eat(self, ttype):
        """Consume the current token if it matches ttype, else raise."""
        tok = self._current()
        if tok.type != ttype:
            raise SyntaxError(
                f"Expected {ttype.name} but got {tok.type.name} ({tok.value!r})"
            )
        self.pos += 1
        return tok

    def _peek(self):
        return self._current().type

    # --- grammar rules -----------------------------------------------------

    def parse(self):
        """Entry point — parse a full expression and check nothing is left."""
        node = self._expr()
        self._eat(TokenType.EOF)
        return node

    def _expr(self):
        """expr → term (('+' | '-') term)*"""
        node = self._term()
        while self._peek() in (TokenType.PLUS, TokenType.MINUS):
            op   = self._eat(self._peek())
            node = BinOpNode(node, op, self._term())
        return node

    def _term(self):
        """term → factor (('*' | '/') factor)*"""
        node = self._factor()
        while self._peek() in (TokenType.MUL, TokenType.DIV):
            op   = self._eat(self._peek())
            node = BinOpNode(node, op, self._factor())
        return node

    def _factor(self):
        """factor → base ('^' factor)*   (right-associative)"""
        base = self._base()
        if self._peek() == TokenType.POWER:
            op  = self._eat(TokenType.POWER)
            exp = self._factor()          # recurse for right-associativity
            return BinOpNode(base, op, exp)
        return base

    def _base(self):
        """base → NUMBER | '(' expr ')' | unary +/-"""
        tok = self._current()

        if tok.type == TokenType.NUMBER:
            self._eat(TokenType.NUMBER)
            return NumberNode(tok.value)

        if tok.type == TokenType.LPAREN:
            self._eat(TokenType.LPAREN)
            node = self._expr()
            self._eat(TokenType.RPAREN)
            return node

        if tok.type in (TokenType.PLUS, TokenType.MINUS):
            op = self._eat(tok.type)
            return UnaryOpNode(op, self._base())

        raise SyntaxError(
            f"Unexpected token {tok.type.name} ({tok.value!r})"
        )