import enum
import queue

EPSILON_SYMBOL = "$"
DFA = "DFA"
NFA = "NFA"

class State():

    def __init__(self, name):
        self.name = name
        self.transitions = set()
        self.worked = False

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name < other.name

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def add_transition(self, target: str, symbol: str):
        self.transitions.add(Transition(self.name, target, symbol))
class Transition():

    def __init__(self, origin: str, target: str, symbol: str):
        self.origin = origin
        self.target = target
        self.symbol = symbol

    def __hash__(self):
        return hash(self.render())

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.origin == other.origin and self.symbol == other.symbol and self.target == other.target

    def __lt__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.render() < other.render()

    def __str__(self):
        return self.render()

    def render(self) -> str:
        return f"{self.origin}:{self.symbol}>{self.target}"


class operationID(enum.Enum):
    INVALID = 0
    STATES = 1
    INITIAL = 2
    ACCEPT = 3
    ALPHABET = 4
    TRANSITIONS = 5
    

class Automaton():

    def __init__(self, states=None, initial=None, accept=None, alphabet=None, from_file=None):
        self.states = states
        self.initial = initial
        self.accept = accept
        self.alphabet = alphabet
        self._transitions = []
        self.errors = []
        self._has_epsilon = False
        self.exec_path = DFA
        if from_file:
            self.states = set()
            self.initial = ""
            self.accept = set()
            self.alphabet = set()
            self._parse_file(from_file)
        else:
            self._parse_transitions_from_states()
        self.is_valid = self.validate()
        self.remove_unused_states()

    def validate(self) -> bool:
        #initial state is undefined
        if self.initial == "":
            self.errors.append("Initial state not defined")
        if State(self.initial) not in self.states:
            self.errors.append("Invalid initial state")
        #accept state has to exist in states
        for sa in self.accept:
            if State(sa) not in self.states:
                self.errors.append("Invalid initial state")
        #validate if states of transitions are valid
        for trans in self._transitions:
            origin = self.get_state(trans.origin)
            target = self.get_state(trans.target)
            if origin is None:
                self.errors.append(f"Transition has invalid origin state {trans.origin}")
            elif target is None:
                self.errors.append(f"Transition has invalid target state {trans.target}")
            elif trans.symbol != EPSILON_SYMBOL and trans.symbol not in self.alphabet:
                self.errors.append(f"Transition has undefined symbol in alphabet: {trans.symbol}")
            else:
                origin.add_transition(target.name, trans.symbol)
                if trans.symbol == EPSILON_SYMBOL:
                    self._has_epsilon = True
                    self.exec_path = NFA
        for state in self.states:
            if len(state.transitions) != len(self.alphabet):
                self.exec_path = NFA
            for symbol in self.alphabet:
                found = False
                for trans in state.transitions:
                    if trans.symbol == symbol:
                        found = True
                        break
                if not found:
                    self.exec_path = NFA
                    break
        if not self.errors:
            return True
        return False

    def without_epsilon(self) -> "Automaton":
        epsilon_closure = dict()
        states = set()

        for s in self.states:
            s.worked = False

        for s in sorted(self.states):
            target = s.name
            for trans in sorted(s.transitions, key=lambda x: x.target):
                if trans.symbol == EPSILON_SYMBOL: 
                    target = dfs(s, self.states)

            ctarget = format_state_name(target, self.states)
            prev_target = epsilon_closure.get(s.name, None)

            if prev_target == None or len(prev_target) < states:
                epsilon_closure.update({s.name:ctarget})

        for s in sorted(self.states):
            state = State(s.name)
            for trans in s.transitions:
                if trans.symbol != EPSILON_SYMBOL:
                    state.add_transition(trans.target,trans.symbol)
            
            ctarget = epsilon_closure.get(state.name)

            #Augmented transition
            for alph in self.alphabet:
                target = None
                for inner_states in self.states:
                    # Get the Augmented transition
                    if inner_states.name in ctarget:
                        #Get the transitions from the epsilon_closure
                        for trans in inner_states.transitions:
                            if trans.symbol != alph:
                                continue

                            if target == None:
                                target = epsilon_closure.get(trans.target)
                            else:
                                target += epsilon_closure.get(trans.target)

                if target != None:
                    new_targets = format_state_name(target, self.states)

                    for st2 in sorted(self.states):
                        if st2.name in new_targets:
                            state.add_transition(st2.name,alph)
                    
            states.add(state)

        result = Automaton(states, self.initial, self.accept, self.alphabet)

        return result
        
    def as_DFA(self) -> "Automaton":

        if self.exec_path == NFA:

            automaton = self
            if automaton._has_epsilon:
                automaton = self.without_epsilon()

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
                                target = format_state_name(target + trans.target, automaton.states)

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

            accept = set()
            for a in automaton.accept:
                for ast in states:
                    if a in ast.name:
                        accept.add(ast.name)

            return Automaton(states, automaton.initial, accept, automaton.alphabet)

        return self

    def remove_unused_states(self):
        for state in self.states:
            state.worked = False

        bfs(self.initial, self.states)

        visited_states = set()
        for state in self.states:
            if state.worked:
                visited_states.add(state)
            else:
                if state.name in self.accept:
                    self.accept.remove(state.name)
                new_trans = set()
                for trans in self._transitions:
                    if trans.origin != state.name:
                        new_trans.add(trans)
                self._transitions = new_trans

        self.states = visited_states

    def get_state(self, state_name) -> State:
        for state in self.states:
            if state.name == state_name:
                return state
        return None

    def get_states_name(self) -> list:
        names = []
        for state in sorted(self.states):
            names.append(state.name)
        return names

    def _parse_transitions_from_states(self) -> list:
        for state in sorted(self.states):
            for trans in state.transitions:
                self._transitions.append(trans)

    def render(self) -> str:
        output = "#states\n"
        for state in sorted(self.states):
            output += f"{state}\n"
        output += f"#initial\n{self.initial}\n"
        output += "#accepting\n"
        for accept in sorted(self.accept):
            output += f"{accept}\n"
        output += "#alphabet\n"
        for symbol in sorted(self.alphabet):
            output += f"{symbol}\n"
        output += "#transitions\n"
        for trans in self._transitions:
            output += f"{trans.render()}\n"
        return output

    def _parse_file(self, filename):
        parsingID = operationID.INVALID
        with open(filename, "r") as f:
            for x in f:
                x = x.strip()
                if x[0] == '#':
                    if(x == '#states'):
                        #Parsing states elements 
                        parsingID = operationID.STATES
                    elif (x == '#initial'):
                        #parsing initial elements
                        parsingID = operationID.INITIAL
                    elif (x == '#accepting'):
                        #parsing accepting elements
                        parsingID = operationID.ACCEPT
                    elif(x == '#alphabet'):
                        #Parsing alphabet elements
                        parsingID = operationID.ALPHABET
                    elif(x == '#transitions'):
                        #Parsing transition elements
                        parsingID = operationID.TRANSITIONS
                    else:
                        # Invalid #operation
                        parsingID = operationID.INVALID
                        self.errors.append(f"Parsing section not supported: {x}")
                else:
                    #Parsing states elements
                    if (parsingID == operationID.STATES):
                        self.states.add(State(x))
                    #Parsing initial elements
                    #you only can have one state of initial
                    elif (parsingID == operationID.INITIAL):
                        if self.initial == "":
                            self.initial = x
                        else:
                            self.errors.append("More than one initial state")
                    #Parsing accepting elements
                    elif (parsingID == operationID.ACCEPT):
                        self.accept.add(x)
                    #Parsing alphabet elements
                    elif (parsingID == operationID.ALPHABET):
                        self.alphabet.add(x)
                    #Parsing transition elements
                    elif (parsingID == operationID.TRANSITIONS):
                        try:
                            s = x.split(':')
                            origin = s[0]
                            a = s[1].split('>')
                            symbol = a[0]
                            for target in a[1].split(','):
                                self._transitions.append(Transition(origin, target, symbol))
                        except:
                            self.errors.append(f"Invalid transition definition: {x}")


def format_state_name(name: str, states: set) -> str:
    new_name = None
    for state in sorted(states):
        if state.name in name:
            if new_name == None:
                new_name = state.name
            else:
                new_name += state.name
    return new_name


def get_new_transitions(automaton: Automaton, st: State) -> dict:
    new_trans = {}        
    for state in sorted(automaton.states):    
        if state.name not in st.name:
            continue

        for trans in state.transitions:
            prev = new_trans.get(trans.symbol)
            if prev is None:
                new_trans[trans.symbol] = trans.target
            else:
                new_trans[trans.symbol] = format_state_name(prev + trans.target, automaton.states)
    
    return new_trans


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