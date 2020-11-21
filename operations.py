from itertools import product

from automaton import Automaton, State

def union(automaton1: Automaton, automaton2: Automaton) -> Automaton:
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
    states = get_states_cross_product(automaton1, automaton2)
    initial = automaton1.initial + automaton2.initial
    accept = set()
    for a1 in automaton1.accept:
        for a2 in automaton2.accept:
            accept.add(a1+a2)
    alphabet = automaton1.alphabet | automaton2.alphabet
    return Automaton(states, initial, accept, alphabet)


def concat(automaton1: Automaton, automaton2: Automaton) -> Automaton:
    # TODO: Implement this
    raise NotImplementedError


def kleene_star(automaton1: Automaton) -> Automaton:
    # TODO: Implement this
    raise NotImplementedError

def get_states_cross_product(automaton1: Automaton, automaton2: Automaton) -> set:
    states = set()
    for s1 in sorted(automaton1.states):
        for s2 in sorted(automaton2.states):
            state = State(f"{s1.name}{s2.name}")
            for trans1 in s1.transitions:
                for trans2 in s2.transitions:
                    if trans1.symbol == trans2.symbol:
                        state.add_transition(f"{trans1.target}{trans2.target}", trans1.symbol)
            states.add(state)
    return states
