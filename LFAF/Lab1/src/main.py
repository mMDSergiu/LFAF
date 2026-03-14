import random

# Grammar class represents a regular grammar
class Grammar:

    def __init__(self):
        # non-terminal symbols
        self.VN = ['S', 'B', 'D']

        # terminal symbols
        self.VT = ['a', 'b', 'c']

        # start symbol
        self.S = 'S'

        # production rules stored as dictionary
        self.P = {
            'S': ['aB', 'bB'],
            'B': ['bD', 'cB', 'aS'],
            'D': ['b', 'aD']
        }

    # generate a valid string using the grammar rules
    def generate_string(self):

        # start with start symbol
        current = self.S

        # continue replacing non-terminals
        while True:

            # find first non-terminal
            index = -1
            for i in range(len(current)):
                if current[i] in self.VN:
                    index = i
                    break

            # if no non-terminals remain stop
            if index == -1:
                break

            symbol = current[index]

            # choose random production rule
            production = random.choice(self.P[symbol])

            # replace non-terminal with chosen production
            current = current[:index] + production + current[index+1:]

        return current

    # convert grammar to finite automaton
    def to_finite_automaton(self):

        states = self.VN + ['F']
        alphabet = self.VT
        start_state = self.S
        final_states = ['F']

        transitions = {}

        # convert productions into transitions
        for left in self.P:
            for rule in self.P[left]:

                if len(rule) == 2:
                    terminal = rule[0]
                    next_state = rule[1]

                    transitions.setdefault((left, terminal), []).append(next_state)

                elif len(rule) == 1:
                    terminal = rule

                    transitions.setdefault((left, terminal), []).append('F')

        return FiniteAutomaton(states, alphabet, transitions, start_state, final_states)


# Finite Automaton class
class FiniteAutomaton:

    def __init__(self, states, alphabet, transitions, start_state, final_states):

        # set of states
        self.Q = states

        # alphabet
        self.Sigma = alphabet

        # transition function
        self.delta = transitions

        # start state
        self.q0 = start_state

        # final states
        self.F = final_states

    # check if a string belongs to the language
    def string_belongs_to_language(self, input_string):

        current_states = [self.q0]

        for symbol in input_string:

            next_states = []

            for state in current_states:

                if (state, symbol) in self.delta:
                    next_states.extend(self.delta[(state, symbol)])

            current_states = next_states

        # check if any current state is final
        for state in current_states:
            if state in self.F:
                return True

        return False


# main function to test everything
def main():

    grammar = Grammar()

    print("Generated strings:")
    for _ in range(5):
        print(grammar.generate_string())

    automaton = grammar.to_finite_automaton()

    print("\nString validation:")

    test_strings = ["ab", "abb", "acabb", "bbb", "aac"]

    for s in test_strings:
        result = automaton.string_belongs_to_language(s)
        print(s, "->", result)


# run program
if __name__ == "__main__":
    main()
