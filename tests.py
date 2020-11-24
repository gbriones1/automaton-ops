from automaton import Automaton, DFA, NFA
from operations import union, intersect, concat, kleene_star

class TestAutomaton():

    def test_is_valid(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/DFA_2.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/DFA_3.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/NFA_2.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/NFA_3.txt")
        assert a1.is_valid
        a1 = Automaton(from_file="samples/NFA_4.txt")
        assert a1.is_valid

    def test_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert a1.exec_path == DFA
        a1 = Automaton(from_file="samples/DFA_2.txt")
        assert a1.exec_path == DFA
        a1 = Automaton(from_file="samples/DFA_3.txt")
        assert a1.exec_path == DFA

    def test_NFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert a1.exec_path == NFA
        a1 = Automaton(from_file="samples/NFA_2.txt")
        assert a1.exec_path == NFA
        a1 = Automaton(from_file="samples/NFA_3.txt")
        assert a1.exec_path == NFA
        a1 = Automaton(from_file="samples/NFA_4.txt")
        assert a1.exec_path == NFA

    def test_without_epsilon(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert not a1._has_epsilon
        a2 = a1.without_epsilon()
        assert not a2._has_epsilon
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1._has_epsilon
        a2 = a1.without_epsilon()
        assert not a2._has_epsilon
        a1 = Automaton(from_file="samples/NFA_2.txt")
        assert a1._has_epsilon
        a2 = a1.without_epsilon()
        assert not a2._has_epsilon
        a1 = Automaton(from_file="samples/NFA_4.txt")
        assert a1._has_epsilon
        a2 = a1.without_epsilon()
        assert not a2._has_epsilon

    def test_as_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert a1.exec_path == DFA
        a2 = a1.as_DFA()
        assert a2.exec_path == DFA
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert a1.exec_path == NFA
        a2 = a1.as_DFA()
        assert a2.exec_path == DFA
        a1 = Automaton(from_file="samples/NFA_2.txt")
        assert a1.exec_path == NFA
        a2 = a1.as_DFA()
        assert a2.exec_path == DFA
        a1 = Automaton(from_file="samples/NFA_3.txt")
        assert a1.exec_path == NFA
        a2 = a1.as_DFA()
        assert a2.exec_path == DFA
        a1 = Automaton(from_file="samples/NFA_4.txt")
        assert a1.exec_path == NFA
        a2 = a1.as_DFA()
        assert a2.exec_path == DFA


class TestUnion():

    def test_DFA_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = union(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid

    def test_NFA_DFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = union(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid

    def test_NFA_NFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/NFA_2.txt")
        assert not a2.errors
        result = union(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid


class TestIntersect():

    def test_DFA_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = intersect(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid

    def test_NFA_DFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = intersect(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid

    def test_NFA_NFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/NFA_2.txt")
        assert not a2.errors
        result = intersect(a1, a2)
        assert result.exec_path == DFA
        assert result.is_valid

class TestConcat():

    def test_DFA_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = concat(a1, a2)
        assert result.exec_path == NFA
        assert result.is_valid

    def test_NFA_DFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/DFA_2.txt")
        assert not a2.errors
        result = concat(a1, a2)
        assert result.exec_path == NFA
        assert result.is_valid

    def test_NFA_NFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        a2 = Automaton(from_file="samples/NFA_2.txt")
        assert not a2.errors
        result = concat(a1, a2)
        assert result.exec_path == NFA
        assert result.is_valid

class TestKleeneStar():

    def test_DFA(self):
        a1 = Automaton(from_file="samples/DFA_1.txt")
        assert not a1.errors
        result = kleene_star(a1)
        assert result.exec_path == NFA
        assert result.is_valid

    def test_NFA(self):
        a1 = Automaton(from_file="samples/NFA_1.txt")
        assert not a1.errors
        result = kleene_star(a1)
        assert result.exec_path == NFA
        assert result.is_valid