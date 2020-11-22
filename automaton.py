import enum

EPSILON_SYMBOL = "$"

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

    def render(self) -> str:
        return f"{self.origin}:{self.symbol}>{self.target}"

    def __str__(self):
        return self.render()


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
        if from_file:
            self.states = set()
            self.initial = ""
            self.accept = set()
            self.alphabet = set()
            self._parse_file(from_file)
        else:
            self._parse_transitions_from_states()
        self.is_valid = self.validate()

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
        # TODO: Remove unreachable states
        if not self.errors:
            return True
        return False

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
    
