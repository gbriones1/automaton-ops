from itertools import product

from automaton import Automaton, State, EPSILON_SYMBOL

import queue

def union(automaton1n: Automaton, automaton2n: Automaton) -> Automaton:

    if automaton1n._has_epsilon or not is_afd(automaton1n):
        automaton1 = get_dfa_from_nfa(automaton1n)
    else:
        automaton1 = automaton1n
    
    if automaton2n._has_epsilon or not is_afd(automaton2n):
        automaton2 = get_dfa_from_nfa(automaton2n)
    else:
        automaton2 = automaton2n

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


def intersect(automaton1n: Automaton, automaton2n: Automaton) -> Automaton:

    if automaton1n._has_epsilon or not is_afd(automaton1n):
        automaton1 = get_dfa_from_nfa(automaton1n)      
    else:
        automaton1 = automaton1n
    
    if automaton2n._has_epsilon or not is_afd(automaton2n):
        automaton2 = get_dfa_from_nfa(automaton2n)      
    else:
        automaton2 = automaton2n

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
    states = automaton1.states
    #create a new initial state
    newInitial = State("kleen_initial")
    states.add(newInitial)

    for a1 in automaton1.states:
        #newState = State(a1.name)
        #print("el estado ",newState.name)
        if a1.name in automaton1.accept:
            #print("es de aceptacion", newState.name)
            a1.add_transition(newInitial.name,EPSILON_SYMBOL)

    automaton1.accept.add(newInitial.name)
    newInitial.add_transition(automaton1.initial,EPSILON_SYMBOL)
    return Automaton(states, newInitial.name, automaton1.accept, automaton1.alphabet)

def get_states_cross_product(automaton1: Automaton, automaton2: Automaton) -> set:
    states = set()
    for s1 in sorted(automaton1.states):
        for s2 in sorted(automaton2.states):         
            state = State(f"{s1.name}{s2.name}")
            for trans1 in s1.transitions:
                for trans2 in s2.transitions:
                    if trans1.symbol == trans2.symbol:
                        ctarget = f"{trans1.target}{trans2.target}"
                        state.add_transition(ctarget, trans1.symbol)
            states.add(state)
    return states

def is_afd(automaton: Automaton) -> bool:
    for s1 in sorted(automaton.states):
        if len(s1.transitions) != len(automaton.alphabet):
            return False

        for alph in automaton.alphabet:
            found = False
            for trans in s1.transitions:
                if trans.symbol == alph:
                    found = True

            if not found:
                return False
            
    return True


def get_dfa_from_nfa(automaton: Automaton) -> Automaton:

    if automaton._has_epsilon:
        automaton1 = remove_epsilon(automaton)
    else:
        automaton1 = automaton

    if is_afd(automaton1):
        dfa = automaton1     
    else:
        dfa = remove_repeated_transitions(automaton1)

    return dfa

def clean_target(target: str,alphabet: set) -> str:

    states = None
    for alph in sorted(alphabet):
        if alph.name in target:
            if states == None:
                states = alph.name
            else:
                states += alph.name
    
    return states

def dfs(initial: State, states: set) -> str:
    q1 = queue.Queue()
    node_names = None

    q1.put(initial)

    while not q1.empty():

        s = q1.get()

        if s.worked == False:
            s.worked = True
            if node_names == None:
                node_names = s.name
            else:
                node_names += s.name

            for trans in s.transitions:
                if trans.symbol != EPSILON_SYMBOL:
                    continue
                for st in states:
                    if trans.target == st.name:
                        q1.put(st)
                        break
    
    #Clean previous states
    for s in states:
        s.worked = False

    return node_names

def remove_epsilon(automaton: Automaton) -> Automaton:

    cerradura = dict()
    states = set()

    for s in automaton.states:
        s.worked = False

    for s in sorted(automaton.states):
        target = s.name
        for trans in sorted(s.transitions, key=lambda x: x.target):
            if trans.symbol == EPSILON_SYMBOL: 
                target = dfs(s, automaton.states)

        ctarget = clean_target(target, automaton.states)
        prev_target = cerradura.get(s.name, None)

        if prev_target == None or len(prev_target) < states:
            cerradura.update({s.name:ctarget})

    for s in sorted(automaton.states):
        state = State(s.name)
        for trans in s.transitions:
            if trans.symbol != EPSILON_SYMBOL:
                state.add_transition(trans.target,trans.symbol)
        
        ctarget = cerradura.get(state.name)

        #Augmented transition
        for alph in automaton.alphabet:
            target = None
            for inner_states in automaton.states:
                # Get the Augmented transition
                if inner_states.name in ctarget:
                    #Get the transitions from the cerradura
                    for trans in inner_states.transitions:
                        if trans.symbol != alph:
                            continue

                        if target == None:
                            target = cerradura.get(trans.target)
                        else:
                            target += cerradura.get(trans.target)

            if target != None:
                new_targets = clean_target(target, automaton.states)

                for st2 in sorted(automaton.states):
                    if st2.name in new_targets:
                        state.add_transition(st2.name,alph)
                
        states.add(state)

    result = Automaton(states,automaton.initial,automaton.accept, automaton.alphabet)

    return result

def get_new_transitions(automaton: Automaton, st: State) -> dict:
    my_dict = {}        
    for original_states in sorted(automaton.states):    
        if original_states.name not in st.name:
            continue

        for trans in original_states.transitions:
            prev = my_dict.get(trans.symbol)
            if prev is None:
                my_dict[trans.symbol] = trans.target
            else:
                my_dict[trans.symbol] = clean_target(prev + trans.target, automaton.states)
    
    return my_dict


def remove_repeated_transitions(automaton: Automaton) -> Automaton:

    states = set()

    state = State("empty")
    for alph in automaton.alphabet:
        state.add_transition("empty", alph)
    states.add(state)
    for s in sorted(automaton.states):
        state = State(s.name)
        for alph in sorted(automaton.alphabet):
            found = False
            duplicated = False
            target = "empty"
            for trans in s.transitions:
                if trans.symbol == alph:
                    if not found:
                        found = True
                        target = trans.target
                    else:                                      
                        duplicated = True
                        target = clean_target(target + trans.target, automaton.states)

            if duplicated and (State(target) not in automaton.states):
                states.add(State(target))

            state.add_transition(target, alph)
        
        states.add(state)

    repeat = True
    #Check for the new states created
    while repeat:
        repeat = False
        for st in sorted(states - automaton.states):
            if st.name == "empty" or st.worked:
               continue
            
            st.worked = True
            my_dict = get_new_transitions(automaton, st)

            for alph in automaton.alphabet:
                new_state = my_dict.get(alph, None)
                if new_state != None:
                    st.add_transition(new_state, alph)
                    len1 = len(states)
                    states.add(State(new_state))
                    len2 = len(states)
                    if len1 < len2:
                        repeat = True
                else:
                    st.add_transition("empty", alph)
         
    active_states = remove_unused_states(automaton.initial, states)

    accept = set()
    for a in automaton.accept:
        for ast in active_states:
            if a in ast.name:
                accept.add(ast.name)

    result = Automaton(active_states,automaton.initial,accept, automaton.alphabet)

    return result

def bfs(initial: str, states: set):
    queue = []

    for st in states:
        if initial == st.name:
            queue.append(st)
            break
        
    while len(queue) > 0:

        s = queue.pop()
        if s.worked == False:
            s.worked = True
            for trans in s.transitions:
                for st in states:
                    if trans.target == st.name:
                        queue.append(st)
                        break
                
        
def remove_unused_states(initial: str,states: set) -> set:
    #Clean all the states
    for st in states:
        st.worked = False

    bfs(initial, states)

    used_states = set()

    for st in states:
        if st.worked:
            used_states.add(st)
    
    return used_states
    