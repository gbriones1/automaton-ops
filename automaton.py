import enum

EPSILON_SYMBOL = "$"
class Transition():

    def __init__(self, origin: str, target: str, symbol: str):
        self.origin = origin
        self.target = target
        self.symbol = symbol

    def render(self):
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

    def __init__(self, from_file):
        self.states = []
        self.initial = ""
        self.accept = []
        self.alphabet = []
        self.transitions = []
        self.is_valid = False
        self.errors = []
        self._parse_file(from_file)
        self.validate()
        import pdb; pdb.set_trace()

    def validate(self):
        # TODO: Validate if automaton is valid, if so, set self.is_valid = True
        # if not, add errors to self.errors
        
        #"set" help to see if an element is repeated (if lenght is different from the lenght of the set, this means a element is repeated)
        #states repeated, throw an error
        if len(self.states) != len(set(self.states)):
            self.errors.append("States repeated")
        #initial state is undefined
        if self.initial == "" or self.initial not in self.states:
            self.errors.append("No initial state")
        #accept state has to exist in states
        for sa in self.accept:
            if sa not in self.states:
                self.errors.append("Invalid initial state")
        #alphabet cannot be repeated
        if len(self.alphabet) != len(set(self.alphabet)):
            self.errors.append("Alphabet repeated")
        #validate if states of transitions are valid
        for trans in self.transitions:
            if trans.origin not in self.states:
                self.errors.append(f"Transition has invalid origin state {trans.origin}")
            if trans.target not in self.states:
                self.errors.append(f"Transition has invalid target state {trans.target}")
            if trans.symbol != EPSILON_SYMBOL and trans.symbol not in self.alphabet:
                self.errors.append(f"Transition has undefined symbol in alphabet: {trans.symbol}")
                    

    def render(self):
        # TODO: Return a string in a format accepted by FSM simulator
        pass

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
                else:
                    #Parsing states elements
                    if (parsingID == operationID.STATES):
                        self.states.append(x)
                    #Parsing initial elements
                    #you only can have one state of initial
                    elif (parsingID == operationID.INITIAL):
                        if(self.initial == ""):
                            self.initial = x
                        else:
                            self.errors.append("Missing initial state")
                    #Parsing accepting elements
                    elif (parsingID == operationID.ACCEPT):
                        self.accept.append(x)
                    #Parsing alphabet elements
                    elif (parsingID == operationID.ALPHABET):
                        self.alphabet.append(x)
                    #Parsing transition elements
                    elif (parsingID == operationID.TRANSITIONS):
                        try:
                            s = x.split(':')
                            origin = s[0]
                            a = s[1].split('>')
                            symbol = a[0]
                            for target in a[1].split(','):
                                self.transitions.append(Transition(origin,target,symbol))
                        except:
                            self.errors.append(f"Invalid transition definition: {x}")
                    else:
                        self.errors.append(f"Parsing section not supported: {x}")
    
