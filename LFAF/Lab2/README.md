# Laboratory Work 2 – Finite Automata

Course: Formal Languages & Finite Automata  
Author: Sergiu Cătănoi  
Group: FAF-242

---

# Theory

Finite automata are mathematical models used to represent systems with a finite number of states. They process input strings symbol by symbol and change their state according to defined transition rules.

There are two main types of finite automata: deterministic (DFA) and non-deterministic (NDFA). In a deterministic automaton, each state has at most one transition for each symbol in the alphabet. In a non-deterministic automaton, a transition may lead to multiple states.

Non-deterministic automata can always be transformed into deterministic automata using the subset construction algorithm.

Another important concept is the Chomsky hierarchy, which classifies grammars into four types depending on their production rules. Regular grammars belong to Type 3 in this hierarchy.

---

# Objectives

• Understand the structure of a finite automaton.  
• Determine whether an automaton is deterministic or non-deterministic.  
• Convert a finite automaton into a regular grammar.  
• Convert a non-deterministic automaton into a deterministic automaton.  
• Classify a grammar according to the Chomsky hierarchy.

---

# Implementation description

The project was implemented in Python and contains two main classes: `FiniteAutomaton` and `Grammar`.

The `FiniteAutomaton` class stores the states, alphabet, transitions, start state and final states of the automaton. A function was implemented to determine if the automaton is deterministic by checking if any transition leads to multiple states.

Another function converts the finite automaton into a regular grammar by transforming transitions into production rules. If a transition leads to a final state, an additional production with only the terminal symbol is added.

A subset construction algorithm was implemented to convert the NDFA into a DFA. This algorithm groups states into sets and builds deterministic transitions between them.

The `Grammar` class contains the grammar used in Laboratory Work 1 and includes a function that classifies the grammar according to the Chomsky hierarchy.

Example of the main execution part:

```python
def main():

    fa = FiniteAutomaton()

    print("Is the automaton deterministic?")
    print(fa.is_deterministic())

    grammar = fa.to_regular_grammar()

    states, transitions, start, finals = fa.convert_to_dfa()
```

---

# Conclusions / Screenshots / Results

The implemented program successfully analyzes a finite automaton and determines whether it is deterministic. In this case, the automaton is non-deterministic because one transition leads to multiple states.

The program also converts the finite automaton into an equivalent regular grammar and performs a conversion from NDFA to DFA using the subset construction algorithm.

Example output of the program:

```
Finite Automaton Information

States: {'q2', 'q3', 'q0', 'q1'}
Alphabet: {'a', 'b', 'c'}
Start State: q0
Final States: {'q3'}

Is the automaton deterministic?
False
```

The conversion algorithm also generates DFA states represented as sets of NDFA states.

---

# References

1. Course materials – Formal Languages & Finite Automata  
2. Laboratory work instructions provided by the professor  
3. https://en.wikipedia.org/wiki/Finite-state_machine  
4. https://en.wikipedia.org/wiki/Chomsky_hierarchy