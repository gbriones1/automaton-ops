from itertools import product

from automaton import Automaton, State

import queue

EPSILON_SYMBOL = "$"

def union(automaton1n: Automaton, automaton2n: Automaton) -> Automaton:

    if is_afd(automaton1n):
        automaton1 = automaton1n
    else:
        automaton1 = get_afd_from_afn(automaton1n)
    
    if is_afd(automaton2n):
        automaton2 = automaton2n
    else:
        automaton2 = get_afd_from_afn(automaton2n)

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

    if is_afd(automaton1n):
        automaton1 = automaton1n
    else:
        automaton1 = get_afd_from_afn(automaton1n)
    
    if is_afd(automaton2n):
        automaton2 = automaton2n
    else:
        automaton2 = get_afd_from_afn(automaton2n)

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
    states = set()
    #create a new initial state
    newInitial = State("kleen_initial")
    states.add(newInitial)
    initial = newInitial.name

    for a1 in automaton1.states:
        newState = State(a1.name)
        #print("el estado ",newState.name)
        if newState.name in automaton1.accept:
            #print("es de aceptacion", newState.name)
            newState.add_transition(initial,EPSILON_SYMBOL)
        for t1 in automaton1._transitions:
            if t1.origin == a1.name:
              newState.add_transition(t1.target, t1.symbol)
             #print("target ",t1.target,"transition", t1.symbol)
              
        states.add(newState)
        
    newInitial.add_transition(automaton1.initial,EPSILON_SYMBOL)
    return Automaton(states, initial, automaton1.accept, automaton1.alphabet)

def get_states_cross_product(automaton1: Automaton, automaton2: Automaton) -> set:
    states = set()
    join_set = automaton1.states | automaton2.states
    for s1 in sorted(automaton1.states):
        for s2 in sorted(automaton2.states):         
            state = State(clean_target(f"{s1.name}{s2.name}", join_set))
            for trans1 in s1.transitions:
                for trans2 in s2.transitions:
                    if trans1.symbol == trans2.symbol:
                        ctarget = clean_target(f"{trans1.target}{trans2.target}", join_set)
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
                if trans.symbol == EPSILON_SYMBOL:
                    return False
                elif trans.symbol == alph:
                    found = True

            if not found:
                return False
            
    return True


def has_repeated_transitions(automaton: Automaton) -> bool:
    for s in sorted(automaton.states):
        if len(s.transitions) != len(automaton.alphabet):
            print(f"state {s.name} has {len(s.transitions)} and automaton has {len(automaton.alphabet)}")
            return True

        for alph in automaton.alphabet:
            found = False
            for trans in s.transitions:
                if trans.symbol == alph:
                    if not found:
                        found = True
                    else:
                        return True
                        
    return False

def has_epsilon(automaton: Automaton) -> Automaton:
    for trans in automaton._transitions:
        if trans.symbol == EPSILON_SYMBOL:
            print("Theres an epsilon")
            return True
        
    return False

def get_afd_from_afn(automaton: Automaton) -> Automaton:

    if has_epsilon(automaton):
        automaton1 = remove_epsilon(automaton)
    else:
        automaton1 = automaton

    if has_repeated_transitions(automaton1):
        afd = remove_repeated_transitions(automaton1)
    else:
        afd = automaton1

    return afd

def take_target(elem):
    return elem.target

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

#    for st in states:
#        if initial == st.name:
    q1.put(initial)
#            break
        
#    print(f"Starting dfs")
    while not q1.empty():

        s = q1.get()

#        print(f"Poping {s.name}")
        if s.worked == False:
            s.worked = True
            if node_names == None:
                node_names = s.name
            else:
                node_names += s.name

            for trans in s.transitions:
                if trans.symbol != EPSILON_SYMBOL:
                    continue
#                print(f"Adding {trans.target}")
                for st in states:
                    if trans.target == st.name:
                        q1.put(st)
                        break
    
    #Clean previous states
    for s in states:
        s.worked = False

    print(f"Nodes reached from {st.name} are {node_names}")
    return node_names

def remove_epsilon(automaton: Automaton) -> Automaton:

    cerradura = dict()
    states = set()
#    return automaton

    for s in automaton.states:
        s.worked = False

    for s in sorted(automaton.states):
        target = s.name
        for trans in sorted(s.transitions, key=take_target):
            if trans.symbol == EPSILON_SYMBOL: #and trans.target not in target:
                target = dfs(s, automaton.states)

#                    target += trans.target

        ctarget = clean_target(target, automaton.states)
        prev_target = cerradura.get(s.name, None)

        if prev_target == None or len(prev_target) < states:
            cerradura.update({s.name:ctarget})

    print(cerradura)

    for s in sorted(automaton.states):
        state = State(s.name)
        for trans in s.transitions:
            if trans.symbol != EPSILON_SYMBOL:
                state.add_transition(trans.target,trans.symbol)
        
        ctarget = cerradura.get(state.name)

        #Augmented transition
#        print(f"Adding {ctarget}")
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

            #Not needed put for debugging purposes
            if target != None:
                new_targets = clean_target(target, automaton.states)

#            print(f"Adding {new_targets} to {state.name} with symbol {alph}")

                for st2 in sorted(automaton.states):
                    if st2.name in new_targets:
                        state.add_transition(st2.name,alph)
                
        states.add(state)

    result = Automaton(states,automaton.initial,automaton.accept, automaton.alphabet)

#    print("After epsilon removal")
#    print(result.render())

    return result

def get_new_transitions(automaton: Automaton, st: State) -> dict:
    my_dict = {}        
    for original_states in sorted(automaton.states):    
        if original_states.name not in st.name:
#            print(f"State {original_states.name} not in {st.name}")
            continue

        for trans in original_states.transitions:
            prev = my_dict.get(trans.symbol)
#            print(f"Adding {trans.target} to {st.name} {trans.symbol} prev = {prev}")
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
        print(f"In state {state}")
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

            #TODO: Check for the original states instead of len
            if duplicated and len(target) > len(alph):
                print(f"Adding State {target}")
                states.add(State(target))

            print(f"Adding transition {state.name}:{alph}>{target}")

            state.add_transition(target, alph)
        
        states.add(state)

    repeat = True
    #Check for the new states created
    while repeat:
        repeat = False
#        print(f"Starting repeat loop")
        for st in sorted(states - automaton.states):
#            print(f"State {st.name}")
            if st.name == "empty" or st.worked:
               continue
            
            st.worked = True
            my_dict = get_new_transitions(automaton, st)

#            print(f"State {st.name} {my_dict}")
            for alph in automaton.alphabet:
                #new_state = ''.join(sorted(set(my_dict[alph]))
                new_state = my_dict.get(alph, None)
                if new_state != None:
                    st.add_transition(new_state, alph)
                    len1 = len(states)
                    states.add(State(new_state))
                    len2 = len(states)
#                print(f"Adding new state: {new_state}, previous len {len1} after adding {len2}")
                    if len1 < len2:
                        repeat = True
                else:
                    st.add_transition("empty", alph)
                    print(f"ERROR: dictionary {my_dict} doesn't have values for key {alph} for state {st.name}")       

            
    accept = set()
    for a in automaton.accept:
        for ast in states:
            if a in ast.name:
                accept.add(ast.name)

#    print("Original Automaton")
#    print(automaton.render())

    active_states = remove_unused_states(automaton.initial, states)
#    active_states = states
#    print(f"States {states}")
#    print(f"Active states {active_states}")
    #Testing:
    result = Automaton(active_states,automaton.initial,accept, automaton.alphabet)

#    print("Removing duplicated transitions")
    print(result.render())

    return result

def bfs(initial: str, states: set):
    queue = []

    for st in states:
        if initial == st.name:
            queue.append(st)
            break
        
#    print(f"Starting bfs")
    while len(queue) > 0:

        s = queue.pop()

#        print(f"Poping {s.name}")
        if s.worked == False:
            s.worked = True
            for trans in s.transitions:
#                print(f"Adding {trans.target}")
                for st in states:
                    if trans.target == st.name:
                        queue.append(st)
                        break
                
        
def remove_unused_states(initial: str,states: set) -> set:
    #Clean all the states
    for st in states:
        st.worked = False

#    print("Calling bfs")
    bfs(initial, states)

    used_states = set()

    for st in states:
#        print(f"State {st.name} active? {st.worked}")
        if st.worked:
            used_states.add(st)
    
    return used_states
    