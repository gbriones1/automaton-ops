from itertools import product

from automaton import Automaton, State, EPSILON_SYMBOL

import queue

def union(automaton1: Automaton, automaton2: Automaton) -> Automaton:
    automaton1 = automaton1.as_DFA()
    automaton2 = automaton2.as_DFA()
    states = get_states_cross_product(automaton1, automaton2)
    initial = automaton1.initial + automaton2.initial
    accept = set()
    for a1 in automaton1.accept:
        for s2 in automaton2.get_states_name():
            accept.add(a1+s2)
    for a2 in automaton2.accept:
        for s1 in automaton1.get_states_name():
            accept.add(s1+a2)
    alphabet = automaton1.alphabet | automaton2.alphabet
    return Automaton(states, initial, accept, alphabet)


def intersect(automaton1: Automaton, automaton2: Automaton) -> Automaton:
    automaton1 = automaton1.as_DFA()
    automaton2 = automaton2.as_DFA()
    states = get_states_cross_product(automaton1, automaton2)
    initial = automaton1.initial + automaton2.initial
    accept = set()
    for a1 in automaton1.accept:
        for a2 in automaton2.accept:
            accept.add(a1+a2)
    alphabet = automaton1.alphabet | automaton2.alphabet
    return Automaton(states, initial, accept, alphabet)


def concat(automaton1: Automaton, automaton2: Automaton) -> Automaton:
    states = set()
    for state in sorted(automaton1.states):
        new_state = State(f"A1{state.name}")
        for trans in state.transitions:
            new_state.add_transition(f"A1{trans.target}", trans.symbol)
        if state.name in automaton1.accept:
            new_state.add_transition(f"A2{automaton2.initial}", EPSILON_SYMBOL)
        states.add(new_state)
    for state in sorted(automaton2.states):
        new_state = State(f"A2{state.name}")
        for trans in state.transitions:
            new_state.add_transition(f"A2{trans.target}", trans.symbol)
        states.add(new_state)
    initial = f"A1{automaton1.initial}"
    accept = set()
    for state_name in automaton2.accept:
        accept.add(f"A2{state_name}")
    alphabet = automaton1.alphabet | automaton2.alphabet
    return Automaton(states, initial, accept, alphabet)


def kleene_star(automaton1: Automaton) -> Automaton:
    states = automaton1.states
    newInitial = State("kleen_initial")
    states.add(newInitial)

    for state in automaton1.states:
        if state.name in automaton1.accept:
            state.add_transition(newInitial.name, EPSILON_SYMBOL)

    automaton1.accept.add(newInitial.name)
    newInitial.add_transition(automaton1.initial, EPSILON_SYMBOL)
    return Automaton(states, newInitial.name, automaton1.accept, automaton1.alphabet)

def get_states_cross_product(automaton1: Automaton, automaton2: Automaton) -> set:
    states = set()
    for s1 in sorted(automaton1.states):
        for s2 in sorted(automaton2.states):         
            state = State(f"{s1.name}{s2.name}")
            for trans1 in s1.transitions:
                for trans2 in s2.transitions:
                    if trans1.symbol == trans2.symbol:
                        target_name = f"{trans1.target}{trans2.target}"
                        state.add_transition(target_name, trans1.symbol)
            states.add(state)
    return states
