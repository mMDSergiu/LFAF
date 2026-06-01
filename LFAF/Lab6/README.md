# Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Cătănoi Sergiu
Group: FAF-242

---

## Theory

**Parsing** is the process of analysing a sequence of tokens to determine its grammatical structure according to a formal grammar. The output is typically a **parse tree** or an **Abstract Syntax Tree (AST)**.

An **Abstract Syntax Tree** is a hierarchical data structure that represents the syntactic structure of source text, stripping away irrelevant details (whitespace, redundant parentheses) and keeping only the semantic relationships. Each internal node represents an operator or construct, and each leaf represents an operand or literal.

A **recursive-descent parser** is a top-down parser where each grammar rule is implemented as a function that calls other functions for sub-rules. Operator precedence is enforced naturally by the call hierarchy — lower-precedence rules call higher-precedence ones.

The grammar used in this lab (arithmetic expressions):

```
expr    → term   (('+' | '-') term)*
term    → factor (('*' | '/') factor)*
factor  → base   ('^' factor)*          -- right-associative
base    → NUMBER | '(' expr ')' | ('+' | '-') base
```

---

## Objectives

1. Get familiar with parsing and how it can be programmed.
2. Get familiar with the concept of an Abstract Syntax Tree (AST).
3. Implement a `TokenType` enum with regex-based categorisation.
4. Implement AST node data structures for arithmetic expressions.
5. Implement a recursive-descent parser that builds the AST from a token stream.

---

## Implementation Description

The implementation is split across four files: `lexer.py`, `ast_nodes.py`, `parser.py`, and `main.py`.

### `lexer.py` — Tokenizer

`TokenType` is a Python `Enum` where each member represents one category of token. All tokens are identified using regular expressions compiled once at module load, applied left-to-right via `re.match`. Whitespace is silently skipped. An `EOF` sentinel token is appended at the end to simplify the parser's termination check.

```python
class TokenType(Enum):
    NUMBER  = auto()   # integer or float literal
    PLUS    = auto()   # +
    MINUS   = auto()   # -
    MUL     = auto()   # *
    DIV     = auto()   # /
    POWER   = auto()   # ^
    LPAREN  = auto()   # (
    RPAREN  = auto()   # )
    EOF     = auto()   # end of input

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
```

### `ast_nodes.py` — AST Node Classes

Three node types cover all arithmetic constructs. Each stores the minimum information needed to reconstruct the expression's meaning:

```python
class NumberNode:
    """Leaf — a numeric literal."""
    def __init__(self, value): self.value = float(value)

class BinOpNode:
    """Binary operation: left OP right."""
    def __init__(self, left, op, right):
        self.left = left; self.op = op; self.right = right

class UnaryOpNode:
    """Unary negation or promotion: OP operand."""
    def __init__(self, op, operand):
        self.op = op; self.operand = operand
```

### `parser.py` — Recursive-Descent Parser

The `Parser` class holds the token list and a current-position cursor. Each grammar rule is one method. `_eat` consumes and returns the current token if its type matches, raising `SyntaxError` otherwise. Precedence is enforced by the call chain: `_expr` → `_term` → `_factor` → `_base`; higher in the chain means lower precedence.

```python
def _expr(self):
    """expr → term (('+' | '-') term)*"""
    node = self._term()
    while self._peek() in (TokenType.PLUS, TokenType.MINUS):
        op   = self._eat(self._peek())
        node = BinOpNode(node, op, self._term())
    return node

def _factor(self):
    """factor → base ('^' factor)*   -- right-associative via recursion"""
    base = self._base()
    if self._peek() == TokenType.POWER:
        op  = self._eat(TokenType.POWER)
        exp = self._factor()      # recurse instead of loop = right-assoc
        return BinOpNode(base, op, exp)
    return base
```

The key design choice for right-associativity of `^` is using **recursion** in `_factor` instead of a `while` loop. A `while` loop would produce left-associative trees (`(2^3)^2`), while recursion naturally produces right-associative trees (`2^(3^2)`).

### `main.py` — Entry Point

Ties the three components together: calls `tokenize`, passes the token list to `Parser`, and pretty-prints the resulting AST recursively with indentation to make the tree structure visible.

---

## Conclusions / Screenshots / Results

Six test expressions with their token streams and ASTs:

**`3 + 5`**
```
Tokens: NUMBER(3)  PLUS  NUMBER(5)  EOF
AST:
BinOp('+')
  Number(3.0)
  Number(5.0)
```

**`10 - 2 * 3`** — multiplication binds tighter than subtraction:
```
AST:
BinOp('-')
  Number(10.0)
  BinOp('*')
    Number(2.0)
    Number(3.0)
```

**`(1 + 2) * (3 + 4)`** — parentheses override precedence:
```
AST:
BinOp('*')
  BinOp('+')
    Number(1.0)
    Number(2.0)
  BinOp('+')
    Number(3.0)
    Number(4.0)
```

**`2 ^ 3 ^ 2`** — right-associative, parsed as `2 ^ (3 ^ 2)`:
```
AST:
BinOp('^')
  Number(2.0)
  BinOp('^')
    Number(3.0)
    Number(2.0)
```

**`-5 + 3`** — unary minus becomes a `UnaryOpNode`:
```
AST:
BinOp('+')
  UnaryOp('-')
    Number(5.0)
  Number(3.0)
```

**`3.14 * (2 + 1)`** — float literals supported:
```
AST:
BinOp('*')
  Number(3.14)
  BinOp('+')
    Number(2.0)
    Number(1.0)
```

All test cases produce correct trees. The main difficulty was implementing right-associativity for the `^` operator — using a `while` loop (as for `+`, `-`, `*`, `/`) would make it left-associative, so `_factor` recurses into itself instead, which naturally folds to the right.

---

## References

- [Parsing — Wikipedia](https://en.wikipedia.org/wiki/Parsing)
- [Abstract Syntax Tree — Wikipedia](https://en.wikipedia.org/wiki/Abstract_syntax_tree)
- Formal Languages and Finite Automata course materials, Technical University of Moldova
- [DrVasile/FLFA-Labs](https://github.com/DrVasile/FLFA-Labs) — lab task repository