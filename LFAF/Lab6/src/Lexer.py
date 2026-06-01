"""
Lexer — tokenizes arithmetic expressions.
Uses regex-based TokenType enum for categorization.
"""

import re
from enum import Enum, auto


class TokenType(Enum):
    NUMBER     = auto()   # integer or float literal
    PLUS       = auto()   # +
    MINUS      = auto()   # -
    MUL        = auto()   # *
    DIV        = auto()   # /
    POWER      = auto()   # ^
    LPAREN     = auto()   # (
    RPAREN     = auto()   # )
    EOF        = auto()   # end of input


# Maps regex pattern → TokenType (order matters: longer/specific first)
TOKEN_PATTERNS = [
    (r'\d+(\.\d+)?', TokenType.NUMBER),
    (r'\+',          TokenType.PLUS),
    (r'-',           TokenType.MINUS),
    (r'\*',          TokenType.MUL),
    (r'/',           TokenType.DIV),
    (r'\^',          TokenType.POWER),
    (r'\(',          TokenType.LPAREN),
    (r'\)',          TokenType.RPAREN),
]

# Compile all patterns once
COMPILED = [(re.compile(pat), ttype) for pat, ttype in TOKEN_PATTERNS]


class Token:
    def __init__(self, ttype, value):
        self.type  = ttype
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


def tokenize(text):
    """
    Scan `text` left-to-right, skipping whitespace, and yield Token objects.
    Raises ValueError on an unrecognised character.
    """
    pos = 0
    tokens = []
    while pos < len(text):
        # skip whitespace
        if text[pos].isspace():
            pos += 1
            continue

        matched = False
        for pattern, ttype in COMPILED:
            m = pattern.match(text, pos)
            if m:
                tokens.append(Token(ttype, m.group()))
                pos = m.end()
                matched = True
                break

        if not matched:
            raise ValueError(f"Unrecognised character {text[pos]!r} at position {pos}")

    tokens.append(Token(TokenType.EOF, None))
    return tokens