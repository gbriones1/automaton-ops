class Transition():

    def __init__(self, dest: str, target: str, symbol: str):
        self.dest = dest
        self.target = target
        self.symbol = symbol

    def render(self):
        # TODO: Return a string in the format s0:a>s1
        pass

class Automaton():

    def __init__(self, states: list = [], initial: str = "", accept: list = [], alphabet: list = [], transitions: list=[], from_file: str = ""):
        self.states = states
        self.initial = initial
        self.accept = accept
        self.alphabet = alphabet
        self.transitions = transitions
        self.is_valid = False
        self.errors = []
        if from_file:
            self._parse_file(from_file)
        self.validate()

    def validate(self):
        # TODO: Validate if automaton is valid, if so, set self.is_valid = True
        # if not, add errors to self.errors
        pass

    def render(self):
        # TODO: Return a string in a format accepted by FSM simulator
        pass

    def _parse_file(self, filename):
        # TODO: Fill attributes accordingly to what was read from file
        pass
