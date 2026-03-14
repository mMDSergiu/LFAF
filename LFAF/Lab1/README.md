# Laboratory Work 1 – Regular Grammar and Finite Automaton

Course: Formal Languages & Finite Automata  
Author: Sergiu Cătănoi 
Group: FAF-242

---

# Theory

A formal language is defined using a set of symbols and rules that describe how valid strings can be formed. A grammar consists of nonterminal symbols, terminal symbols, a start symbol and a set of production rules. These rules describe how symbols can be replaced in order to generate strings that belong to the language.

Regular grammars are a special type of grammar where productions follow a simple structure, usually consisting of a terminal followed by at most one non-terminal. Because of this structure, regular grammars can be converted into finite automata.

A finite automaton is a mathematical model used to recognize patterns in strings. It consists of a set of states, an alphabet, transitions between states, a start state and one or more final states. The automaton processes a string symbol by symbol and determines if the string belongs to the language.

---

# Objectives

• Understand the concept of a formal language and grammar.  
• Implement a class that represents a regular grammar.  
• Generate valid strings using the grammar rules.  
• Convert the grammar into a finite automaton.  
• Implement a function that checks if a string belongs to the language using the finite automaton.

---

# Implementation description

The project was implemented in Python using two main classes: `Grammar` and `FiniteAutomaton`.

The `Grammar` class stores the components of the grammar such as the set of non-terminals, terminals, production rules and the start symbol. A method called `generate_string()` randomly applies production rules starting from the start symbol until no non-terminal symbols remain, producing valid strings from the language.

Another method called `to_finite_automaton()` converts the grammar into an equivalent finite automaton. Each production rule is transformed into a state transition.

The `FiniteAutomaton` class stores the automaton components including states, alphabet, transitions, start state and final states. A method called `string_belongs_to_language()` simulates the automaton and verifies whether a given string can be accepted.

Example of the main part of the program:

```python
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


if __name__ == "__main__":
    main()
    
Conclusions / Screenshots / Results
The program successfully implements a regular grammar and converts it into a finite automaton. The grammar can generate valid strings by applying production rules starting from the start symbol. The finite automaton can then verify whether a given string belongs to the language defined by the grammar.

Example program output:

Generated strings:
babcaabb
baaabcabbab
baaaabaab
bcaabb
bcaaaacccccbb

String validation:
ab -> False
abb -> True
acabb -> False
bbb -> True
aac -> False

References
Course materials – Formal Languages & Finite Automata

Laboratory work instruction

https://en.wikipedia.org/wiki/Formal_grammar

https://en.wikipedia.org/wiki/Finite-state_machine

