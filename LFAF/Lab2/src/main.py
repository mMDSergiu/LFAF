class FiniteAutomaton:

    def __init__(self):

        self.Q = {"q0", "q1", "q2", "q3"}
        self.Sigma = {"a", "b", "c"}
        self.q0 = "q0"
        self.F = {"q3"}

        # transition function for the given variant
        self.delta = {
            ("q0", "a"): ["q1"],
            ("q0", "b"): ["q2"],
            ("q1", "b"): ["q2"],
            ("q1", "a"): ["q3"],
            ("q2", "c"): ["q0", "q3"]
        }

    # checks if the automaton is deterministic
    def is_deterministic(self):

        for transition in self.delta:
            if len(self.delta[transition]) > 1:
                return False

        return True

    # converts the finite automaton into a regular grammar
    def to_regular_grammar(self):

        productions = {}

        for (state, symbol), next_states in self.delta.items():

            if state not in productions:
                productions[state] = []

            for next_state in next_states:

                productions[state].append(symbol + next_state)

                if next_state in self.F:
                    productions[state].append(symbol)

        return productions

    # converts NDFA to DFA using subset construction
    def convert_to_dfa(self):

        start_state = frozenset([self.q0])

        dfa_states = [start_state]
        processed_states = []
        dfa_transitions = {}
        dfa_final_states = []

        while dfa_states:

            current_state = dfa_states.pop(0)
            processed_states.append(current_state)

            for symbol in self.Sigma:

                next_state = set()

                for state in current_state:

                    if (state, symbol) in self.delta:
                        next_state.update(self.delta[(state, symbol)])

                if next_state:

                    next_state = frozenset(next_state)

                    dfa_transitions[(current_state, symbol)] = next_state

                    if next_state not in processed_states and next_state not in dfa_states:
                        dfa_states.append(next_state)

        for state in processed_states:
            if "q3" in state:
                dfa_final_states.append(state)

        return processed_states, dfa_transitions, start_state, dfa_final_states


class Grammar:

    def __init__(self):

        self.VN = {"S", "B", "D"}
        self.VT = {"a", "b", "c"}

        self.P = {
            "S": ["aB", "bB"],
            "B": ["bD", "cB", "aS"],
            "D": ["b", "aD"]
        }

        self.S = "S"

    # classifies the grammar according to the Chomsky hierarchy
    def classify_grammar(self):

        for left in self.P:

            for rule in self.P[left]:

                if len(rule) == 1 and rule in self.VT:
                    continue

                if len(rule) == 2 and rule[0] in self.VT and rule[1] in self.VN:
                    continue

                return "Type 2 - Context Free Grammar"

        return "Type 3 - Regular Grammar"


def main():

    print("Finite Automaton Information\n")

    fa = FiniteAutomaton()

    print("States:", fa.Q)
    print("Alphabet:", fa.Sigma)
    print("Start State:", fa.q0)
    print("Final States:", fa.F)

    print("\nIs the automaton deterministic?")
    print(fa.is_deterministic())

    print("\nFinite Automaton -> Regular Grammar\n")

    grammar = fa.to_regular_grammar()

    for state in grammar:
        print(state, "->", " | ".join(grammar[state]))

    print("\nNDFA -> DFA Conversion\n")

    states, transitions, start, finals = fa.convert_to_dfa()

    print("DFA States:")
    for s in states:
        print(s)

    print("\nDFA Transitions:")
    for key in transitions:
        print(key, "->", transitions[key])

    print("\nDFA Start State:", start)
    print("DFA Final States:", finals)

    print("\nGrammar Classification (from Lab 1 grammar)\n")

    g = Grammar()
    print(g.classify_grammar())


if __name__ == "__main__":
    main()
