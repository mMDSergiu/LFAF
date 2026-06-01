"""
Chomsky Normal Form (CNF) converter.
Variant 11 grammar is the default, but any grammar can be passed in.

Steps performed in order:
  1. Eliminate ε-productions
  2. Eliminate unit (renaming) productions
  3. Eliminate inaccessible symbols
  4. Eliminate non-productive symbols
  5. Convert remaining productions to CNF
"""

from itertools import combinations


VARIANT_11 = {
    'N': {'S', 'A', 'B', 'C', 'D'},
    'T': {'a', 'b'},
    'P': {
        'S': ['bA', 'AC'],
        'A': ['bS', 'BC', 'AbAa'],
        'B': ['BbaA', 'a', 'bSa'],
        'C': [''],        # '' represents ε
        'D': ['AB'],
    },
    'S': 'S',
}


def _tokenize(rhs, non_terminals):
    """
    Split an RHS string into a list of symbol tokens.
    Non-terminals are matched greedily from the known NT set (longest first),
    so multi-char NTs like 'TB' or 'X1' are kept as single tokens.
    """
    tokens = []
    i = 0
    # Sort NTs longest-first so 'TB' is matched before 'T'
    sorted_nts = sorted(non_terminals, key=len, reverse=True)
    while i < len(rhs):
        matched = False
        for nt in sorted_nts:
            if rhs[i:i+len(nt)] == nt:
                tokens.append(nt)
                i += len(nt)
                matched = True
                break
        if not matched:
            tokens.append(rhs[i])   # single-char terminal
            i += 1
    return tokens


# ---------------------------------------------------------------------------
# Step 1 — Eliminate ε-productions
# ---------------------------------------------------------------------------
def eliminate_epsilon(grammar):
    N, T, P, S = grammar['N'], grammar['T'], grammar['P'], grammar['S']

    nullable = set()
    for nt, rules in P.items():
        if '' in rules:
            nullable.add(nt)

    changed = True
    while changed:
        changed = False
        for nt, rules in P.items():
            if nt in nullable:
                continue
            for rhs in rules:
                if rhs and all(sym in nullable for sym in _tokenize(rhs, N)):
                    nullable.add(nt)
                    changed = True

    print(f"  Nullable symbols: {nullable}")

    new_P = {}
    for nt, rules in P.items():
        new_rules = []
        for rhs in rules:
            if rhs == '':
                continue
            tokens = _tokenize(rhs, N)
            nullable_positions = [i for i, sym in enumerate(tokens) if sym in nullable]
            for r in range(len(nullable_positions) + 1):
                for combo in combinations(nullable_positions, r):
                    new_rhs = ''.join(sym for i, sym in enumerate(tokens) if i not in combo)
                    if new_rhs and new_rhs not in new_rules:
                        new_rules.append(new_rhs)
        new_P[nt] = new_rules

    if S in nullable:
        s_on_rhs = any(S in _tokenize(rhs, N) for rules in new_P.values() for rhs in rules)
        if not s_on_rhs:
            new_P[S].append('')

    return {**grammar, 'P': new_P}


# ---------------------------------------------------------------------------
# Step 2 — Eliminate unit (renaming) productions  A → B
# ---------------------------------------------------------------------------
def eliminate_unit_productions(grammar):
    N, T, P, S = grammar['N'], grammar['T'], grammar['P'], grammar['S']

    def unit_closure(nt):
        visited = {nt}
        queue = [nt]
        while queue:
            cur = queue.pop()
            for rhs in P.get(cur, []):
                tokens = _tokenize(rhs, N)
                if len(tokens) == 1 and tokens[0] in N and tokens[0] not in visited:
                    visited.add(tokens[0])
                    queue.append(tokens[0])
        visited.discard(nt)
        return visited

    new_P = {}
    for nt in N:
        new_rules = []
        for rhs in P.get(nt, []):
            tokens = _tokenize(rhs, N)
            if not (len(tokens) == 1 and tokens[0] in N):
                if rhs not in new_rules:
                    new_rules.append(rhs)
        for reachable in unit_closure(nt):
            for rhs in P.get(reachable, []):
                tokens = _tokenize(rhs, N)
                if not (len(tokens) == 1 and tokens[0] in N):
                    if rhs not in new_rules:
                        new_rules.append(rhs)
        new_P[nt] = new_rules

    return {**grammar, 'P': new_P}


# ---------------------------------------------------------------------------
# Step 3 — Eliminate inaccessible symbols
# ---------------------------------------------------------------------------
def eliminate_inaccessible(grammar):
    N, T, P, S = grammar['N'], grammar['T'], grammar['P'], grammar['S']

    reachable = {S}
    queue = [S]
    while queue:
        nt = queue.pop()
        for rhs in P.get(nt, []):
            for sym in _tokenize(rhs, N):
                if sym in N and sym not in reachable:
                    reachable.add(sym)
                    queue.append(sym)

    removed = N - reachable
    if removed:
        print(f"  Inaccessible symbols removed: {removed}")

    new_N = N & reachable
    new_P = {nt: rules for nt, rules in P.items() if nt in reachable}
    return {**grammar, 'N': new_N, 'P': new_P}


# ---------------------------------------------------------------------------
# Step 4 — Eliminate non-productive symbols
# ---------------------------------------------------------------------------
def eliminate_nonproductive(grammar):
    N, T, P, S = grammar['N'], grammar['T'], grammar['P'], grammar['S']

    productive = set()
    for nt, rules in P.items():
        for rhs in rules:
            tokens = _tokenize(rhs, N)
            if rhs == '' or all(sym in T for sym in tokens):
                productive.add(nt)

    changed = True
    while changed:
        changed = False
        for nt, rules in P.items():
            if nt in productive:
                continue
            for rhs in rules:
                tokens = _tokenize(rhs, N)
                if all(sym in T or sym in productive for sym in tokens):
                    productive.add(nt)
                    changed = True

    removed = N - productive
    if removed:
        print(f"  Non-productive symbols removed: {removed}")

    new_N = N & productive
    new_P = {}
    for nt in new_N:
        new_rules = []
        for rhs in P.get(nt, []):
            tokens = _tokenize(rhs, N)
            if all(sym in T or sym in productive for sym in tokens):
                new_rules.append(rhs)
        new_P[nt] = new_rules

    return {**grammar, 'N': new_N, 'P': new_P}


# ---------------------------------------------------------------------------
# Step 5 — Convert to Chomsky Normal Form
# ---------------------------------------------------------------------------
def to_cnf(grammar):
    N, T, P, S = grammar['N'], grammar['T'], grammar['P'], grammar['S']

    new_N = set(N)
    new_P = {nt: list(rules) for nt, rules in P.items()}

    # --- 5a: Replace each terminal in rules of length >= 2 with a fresh NT ---
    terminal_map = {}

    def get_terminal_nt(t):
        if t not in terminal_map:
            name = f'T{t.upper()}'
            while name in new_N:
                name += '_'
            terminal_map[t] = name
            new_N.add(name)
            new_P[name] = [t]
        return terminal_map[t]

    for nt in list(new_P.keys()):
        updated = []
        for rhs in new_P[nt]:
            tokens = _tokenize(rhs, new_N)
            if len(tokens) >= 2:
                new_tokens = []
                for sym in tokens:
                    if sym in T:
                        new_tokens.append(get_terminal_nt(sym))
                    else:
                        new_tokens.append(sym)
                updated.append(''.join(new_tokens))
            else:
                updated.append(rhs)
        new_P[nt] = updated

    # --- 5b: Binarise rules with 3+ symbols (right-to-left) ---
    _counter = [0]

    def fresh_nt():
        _counter[0] += 1
        name = f'X{_counter[0]}'
        while name in new_N:
            _counter[0] += 1
            name = f'X{_counter[0]}'
        return name

    for nt in list(new_P.keys()):
        updated = []
        for rhs in new_P[nt]:
            # Tokenize using the UPDATED new_N so multi-char NTs are recognised
            syms = _tokenize(rhs, new_N)
            while len(syms) > 2:
                new_nt = fresh_nt()
                new_N.add(new_nt)
                # right-to-left: combine last two
                new_P[new_nt] = [''.join(syms[-2:])]
                syms = syms[:-2] + [new_nt]
            updated.append(''.join(syms))
        new_P[nt] = updated

    return {**grammar, 'N': new_N, 'P': new_P}


# ---------------------------------------------------------------------------
# Pretty printer
# ---------------------------------------------------------------------------
def print_grammar(grammar, title="Grammar"):
    P = grammar['P']
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(f"  N = {sorted(grammar['N'])}")
    print(f"  T = {sorted(grammar['T'])}")
    print(f"  S = {grammar['S']}")
    print("  Productions:")
    for nt in sorted(P.keys()):
        rules = P[nt]
        if rules:
            rhs_str = ' | '.join(r if r else 'ε' for r in rules)
            print(f"    {nt} → {rhs_str}")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def normalize_to_cnf(grammar):
    print_grammar(grammar, "Original Grammar")

    print("\n[Step 1] Eliminating ε-productions...")
    g = eliminate_epsilon(grammar)
    print_grammar(g, "After ε-elimination")

    print("\n[Step 2] Eliminating unit (renaming) productions...")
    g = eliminate_unit_productions(g)
    print_grammar(g, "After unit production elimination")

    print("\n[Step 3] Eliminating inaccessible symbols...")
    g = eliminate_inaccessible(g)
    print_grammar(g, "After inaccessible symbol elimination")

    print("\n[Step 4] Eliminating non-productive symbols...")
    g = eliminate_nonproductive(g)
    print_grammar(g, "After non-productive symbol elimination")

    print("\n[Step 5] Converting to Chomsky Normal Form...")
    g = to_cnf(g)
    print_grammar(g, "Final CNF Grammar")

    return g


if __name__ == '__main__':
    normalize_to_cnf(VARIANT_11)