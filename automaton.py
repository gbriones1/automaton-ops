import enum

class Transition():

    def __init__(self, dest: str, target: list=[], symbol: list=[]):
        self.dest = dest
        self.target = target
        self.symbol = symbol

    def render(self):
        # TODO: Return a string in the format s0:a>s1
        pass
        
class operationID(enum.Enum):
    INVALID = 0
    STATES = 1
    INITIAL = 2
    ACCEPT = 3
    ALPHABET = 4
    TRANSITIONS = 5
    
    

class Automaton():

    def __init__(self, states: list = [], initial: str = "", accept: list = [], alphabet: list = [], transitions: list=[], from_file: str = ""):
        self.states = []
        self.initial = ""
        self.accept = []
        #include "$" (epsilon transition) in alphabet
        self.alphabet = ['$']
        self.transitions = []
        self.is_valid = False
        self.errors = []
        if from_file:
            self.initial = ""
            self._parse_file(from_file)
        self.validate()

    def validate(self):
        # TODO: Validate if automaton is valid, if so, set self.is_valid = True
        # if not, add errors to self.errors
        
        #"set" help to see if an element is repeated (if lenght is different from the lenght of the set, this means a element is repeated)
        #states repeated, throw an error
        if len(self.states) != len(set(self.states)):
            raise NotImplementedError
        #initial state is undefined
        if (self.initial == "" or self.initial not in self.states):
            raise NotImplementedError
        #accept state has to exist in states
        for sa in self.accept:
            if(sa not in self.states):
                raise NotImplementedError
        #alphabet cannot be repeated
        if len(self.alphabet) != len(set(self.alphabet)):
            raise NotImplementedError 
        #validate if states of transitions are valid
        for trans in self.transitions:
            if (trans.dest not in self.states):
                print("Invalid destination state")
                raise NotImplementedError
            for tar in trans.target:
                if (tar not in self.states):
                    print("Invalid target state")
                    raise NotImplementedError
            for alpha in trans.symbol:
                if (alpha not in self.alphabet):
                    print("Undefined symbol in alphabet: ", alpha)
                    raise NotImplementedError
                    

    def render(self):
        # TODO: Return a string in a format accepted by FSM simulator
        pass

    def _parse_file(self, filename):
        # TODO: Fill attributes accordingly to what was read from file
            parsingID = operationID.INVALID
            f = open(filename,"r")
            for x in f:
                x = x.strip()
                if(x[0] == '#'):
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
                            raise NotImplementedError
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
                            dest = s[0]
                            a = s[1].split('>')
                            symbol = a[0].split(',')
                            target = a[1].split(',')
                            self.transitions.append(Transition(dest,target,symbol))
                        except:
                            print("Invalid transition definition")
                            raise
                    else:
                        print("not implemented")
                        raise NotImplementedError
            #print("states",self.states)
            #print("initial",self.initial)
            #print("accept",self.accept)
            #print("alphabet",self.alphabet)
            #for x in self.transitions:
                #print("dest ",x.dest," target ",x.target," symbol ",x.symbol)
    
