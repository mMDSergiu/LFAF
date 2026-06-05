import random

MAX_REPEAT = 5  # cap for * and + to avoid infinitely long strings


def parse_and_generate(pattern, trace=False):
    """
    Parses a regex-like pattern and generates a valid random string.
    Supports: (a|b) alternation, + * ? quantifiers, {N} exact repeat.
    Optionally prints a step-by-step processing trace (bonus feature).
    """
    steps = []
    result, _ = _parse(pattern, 0, steps, trace)
    if trace:
        print("\n--- Processing Trace ---")
        for i, step in enumerate(steps, 1):
            print(f"  Step {i}: {step}")
        print(f"  Result: {result}\n")
    return result


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
                break  # closing paren of parent group
            depth -= 1
            current.append(c)
        elif c == '|' and depth == 0:
            parts.append(''.join(current))
            current = []
        else:
            current.append(c)
        i += 1

    parts.append(''.join(current))
    end_pos = i

    if len(parts) > 1:
        chosen = random.choice(parts)
        if trace:
            steps.append(f"Alternation {parts} → chose '{chosen}'")
        result, _ = _parse_sequence(chosen, 0, steps, trace)
    else:
        result, _ = _parse_sequence(parts[0], 0, steps, trace)

    return result, end_pos


def _parse_sequence(pattern, pos, steps, trace):
    """Parses a flat sequence of chars and groups, applying quantifiers."""
    result = ""
    i = 0
    while i < len(pattern):
        c = pattern[i]

        if c == '(':
            # Find matching closing parenthesis
            depth = 1
            j = i + 1
            while j < len(pattern) and depth > 0:
                if pattern[j] == '(':
                    depth += 1
                elif pattern[j] == ')':
                    depth -= 1
                j += 1
            inner = pattern[i+1:j-1]

            # Read quantifier after the closing paren
            quantifier, j = _read_quantifier(pattern, j)

            repeat_count = _resolve_quantifier(quantifier)
            if trace:
                steps.append(f"Group '({inner})' quantifier='{quantifier}' → repeat {repeat_count}x")

            for _ in range(repeat_count):
                part, _ = _parse(inner, 0, steps, trace)
                result += part
            i = j
        else:
            # Single literal character
            char = c
            quantifier, j = _read_quantifier(pattern, i + 1)

            repeat_count = _resolve_quantifier(quantifier)
            if trace:
                steps.append(f"Char '{char}' quantifier='{quantifier}' → repeat {repeat_count}x")

            result += char * repeat_count
            i = j

    return result, i


def _read_quantifier(pattern, pos):
    """
    Reads an optional quantifier starting at pos.
    Returns (quantifier_string_or_None, new_pos).
    Supports: +  *  ?  {N}
    """
    if pos >= len(pattern):
        return None, pos

    c = pattern[pos]
    if c in ('+', '*', '?'):
        return c, pos + 1
    elif c == '{':
        # {N} exact repetition
        k = pos + 1
        num_str = ""
        while k < len(pattern) and pattern[k].isdigit():
            num_str += pattern[k]
            k += 1
        if k < len(pattern) and pattern[k] == '}' and num_str:
            return f'{{{num_str}}}', k + 1

    return None, pos


def _resolve_quantifier(q):
    """Maps a quantifier string to a concrete repeat count."""
    if q is None:
        return 1
    elif q == '?':
        return random.randint(0, 1)
    elif q == '+':
        return random.randint(1, MAX_REPEAT)
    elif q == '*':
        return random.randint(0, MAX_REPEAT)
    elif q.startswith('{') and q.endswith('}'):
        return int(q[1:-1])
    return 1


# --- Variant 1 regexes ---
REGEXES = [
    "(a|b)(c|d)E+G?",       # pick a/b, pick c/d, 1+ E's, optional G
    "P(Q|R|S)T(UV|W|X)+Z",  # P, pick Q/R/S, T, 1+ of UV/W/X, Z
    "1(0|1)*2(3|4){5}36",   # 1, 0+ bits, 2, exactly 5 of 3/4, then 36
]

if __name__ == "__main__":
    print("=== Variant 1: Regular Expression String Generator ===\n")

    for regex in REGEXES:
        print(f"Regex: {regex}")
        print("Generated samples:")
        for _ in range(5):
            print(f"  {parse_and_generate(regex)}")
        print()

    # Bonus: step-by-step trace for one run of each regex
    print("=== Bonus: Processing Traces ===")
    for regex in REGEXES:
        print(f"\nRegex: {regex}")
        parse_and_generate(regex, trace=True)