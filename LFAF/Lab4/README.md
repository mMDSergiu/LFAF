# Regular Expressions — String Generator

### Course: Formal Languages & Finite Automata
### Author: Cătănoi Sergiu
Group: FAF-242

---

## Theory

A **regular expression** (regex) is a formal notation for describing a set of strings using a pattern language. They are built from:

- **Literals** — exact characters to match (e.g. `a`, `3`, `Z`)
- **Alternation** `(a|b)` — match either `a` or `b`
- **Quantifiers** — `+` (one or more), `*` (zero or more), `?` (zero or one), `{N}` (exactly N times)
- **Grouping** `(...)` — treat a sub-expression as a single unit

Regular expressions are widely used in text search, input validation, lexical analysis in compilers, and formal language theory. In this lab, instead of using regex to *match* strings, we **generate** valid strings from a given pattern — essentially interpreting the regex as a grammar.

---

## Objectives

1. Understand what regular expressions are and what they are used for.
2. Implement a dynamic regex interpreter that generates valid strings from a given pattern:
   - Handle alternation `(a|b|c)`
   - Handle quantifiers: `+`, `*`, `?`, `{N}`
   - Cap unbounded quantifiers (`*`, `+`) at 5 repetitions to keep output finite
3. **Bonus**: implement a trace function that shows the processing steps in order.

---

## Implementation Description

### Pattern Parsing (`_parse`)

The top-level parser scans the pattern for `|` operators at depth zero (ignoring `|` inside nested parentheses). It collects all alternatives, randomly picks one, and then delegates to the sequence parser. This cleanly handles any level of nesting.

```python
def _parse(pattern, pos, steps, trace):
    """Handles top-level alternation (|) while respecting parentheses depth."""
    parts = []
    current = []
    depth = 0
    i = pos

    while i < len(pattern):
        c = pattern[i]
        if c == '(':
            depth += 1
            current.append(c)
        elif c == ')':
            if depth == 0:
                break
            depth -= 1
            current.append(c)
        elif c == '|' and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(c)
        i += 1

    parts.append(''.join(current))
    ...
```

### Sequence Processing (`_parse_sequence`)

This function walks the pattern character by character. When it encounters a `(`, it finds the matching `)`, reads the inner expression, then reads any quantifier that follows. For plain characters, it reads the character and any following quantifier. In both cases it calls `_resolve_quantifier` to decide how many times to repeat, then appends the result.

```python
def _parse_sequence(pattern, pos, steps, trace):
    """Parses a flat sequence of chars and groups, applying quantifiers."""
    result = ""
    i = 0
    while i < len(pattern):
        c = pattern[i]
        if c == '(':
            # find closing paren, read inner, read quantifier, repeat inner
            ...
        else:
            # single char, read quantifier, repeat char
            char = c
            quantifier, j = _read_quantifier(pattern, i + 1)
            repeat_count = _resolve_quantifier(quantifier)
            result += char * repeat_count
            i = j
    return result, i
```

### Quantifier Reader (`_read_quantifier`)

A small helper that peeks ahead from a given position and returns the quantifier string (`+`, `*`, `?`, or `{N}`) and the new position after consuming it. This keeps quantifier logic in one place and makes both the group and character branches of the sequence parser clean.

```python
def _read_quantifier(pattern, pos):
    if pos >= len(pattern):
        return None, pos
    c = pattern[pos]
    if c in ('+', '*', '?'):
        return c, pos + 1
    elif c == '{':
        # read digits until closing }
        k = pos + 1
        num_str = ""
        while k < len(pattern) and pattern[k].isdigit():
            num_str += pattern[k]
            k += 1
        if k < len(pattern) and pattern[k] == '}' and num_str:
            return f'{{{num_str}}}', k + 1
    return None, pos
```

### Quantifier Resolver (`_resolve_quantifier`)

Maps the quantifier string to a concrete integer repeat count. Unbounded operators `*` and `+` are capped at `MAX_REPEAT = 5` to prevent excessively long outputs.

```python
def _resolve_quantifier(q):
    if q is None:      return 1
    elif q == '?':     return random.randint(0, 1)
    elif q == '+':     return random.randint(1, MAX_REPEAT)
    elif q == '*':     return random.randint(0, MAX_REPEAT)
    elif q.startswith('{') and q.endswith('}'):
        return int(q[1:-1])
    return 1
```

---

## Conclusions / Screenshots / Results

The three Variant 1 regexes and sample generated outputs:

**Regex 1:** `(a|b)(c|d)E+G?`

```
adEEEG
acEEE
bdEG
adEEEEE
bcEEG
```

**Regex 2:** `P(Q|R|S)T(UV|W|X)+Z`

```
PQTXXXUVZ
PRTUVWZ
PQTWUVXUVXZ
PRTWWWWXZ
PRTUVUVXXUVZ
```

**Regex 3:** `1(0|1)*2(3|4){5}36`

```
1111023344336
10001123444436
11023344436
124434336
10024443436
```

All outputs match the expected patterns from the task description. The implementation is fully dynamic — the regexes are passed in as strings and interpreted at runtime, with no hardcoded generation logic per pattern.

**Bonus trace example** for `(a|b)(c|d)E+G?`:
```
Step 1: Group '(a|b)' quantifier='None' → repeat 1x
Step 2: Alternation ['a', 'b'] → chose 'b'
Step 3: Char 'b' quantifier='None' → repeat 1x
Step 4: Group '(c|d)' quantifier='None' → repeat 1x
Step 5: Alternation ['c', 'd'] → chose 'd'
Step 6: Char 'd' quantifier='None' → repeat 1x
Step 7: Char 'E' quantifier='+' → repeat 4x
Step 8: Char 'G' quantifier='?' → repeat 0x
Result: bdEEEE
```

The main difficulty was ensuring the quantifier `{5}` in `(3|4){5}` was not confused with the literal digit `36` that follows it. This was solved by using `{N}` brace notation in the pattern string and writing a dedicated `_read_quantifier` helper to consume only the quantifier token and nothing beyond it.

---

## References

- Formal Languages and Finite Automata course materials, Technical University of Moldova
- [DrVasile/FLFA-Labs](https://github.com/DrVasile/FLFA-Labs) — lab task repository
- Hopcroft, Motwani, Ullman — *Introduction to Automata Theory, Languages, and Computation*