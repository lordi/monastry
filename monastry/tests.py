import unittest
from interpret import Interpreter

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.i = Interpreter()

    def test_arithmetic(self):
        self.assertEqual(self.i.interpret("()"), [])
        self.assertEqual(self.i.interpret("(4)"), [4])
        self.assertEqual(self.i.interpret("(4 2)"), [4, 2])
        self.assertEqual(self.i.interpret("(4 2 +)"), [6])
        self.assertEqual(self.i.interpret("(4 2 -)"), [2])
        self.assertEqual(self.i.interpret("(5 inc)"), [6])
        self.assertEqual(self.i.interpret("(7 dec)"), [6])

    def test_eval(self):
        self.assertEqual(self.i.interpret("(5 (inc) eval)"), [6])
        self.assertEqual(self.i.interpret("(21 (inc dec) eval)"), [21])

    def test_wrap(self):
        self.assertEqual(self.i.interpret("(2 wrap eval)"), [2])
        self.assertEqual(self.i.interpret("((5 inc) wrap eval eval)"), [6])

    def test_times(self):
        self.assertEqual(self.i.interpret("(4 (2 +) 3 times)"), [10])
        self.assertEqual(self.i.interpret("(13 (inc) 5 times 2 +)"), [20])

    def test_if(self):
        self.assertEqual(self.i.interpret("(20 1 (10 +) if)"), [30])
        self.assertEqual(self.i.interpret("(20 0 (10 +) if)"), [20])

        # inc-lt50 = dup 50 lt (inc) if
        self.assertEqual(self.i.interpret("(45 (dup 50 lt (inc) if) eval)"), [46])
        self.assertEqual(self.i.interpret("(50 (dup 50 lt (inc) if) eval)"), [50])
        self.assertEqual(self.i.interpret("(45 (dup 50 lt (inc) if) 10 times)"), [50])

    def test_swap(self):
        self.assertEqual(self.i.interpret("(10 12 swap lt)"), [0])
        self.assertEqual(self.i.interpret("(50 (inc) swap swap eval)"), [51])

    def test_drop(self):
        self.assertEqual(self.i.interpret("(10 12 14 drop +)"), [22])

    def test_chord(self):
        def _play_note(s):
            #print "play note=", s.pop()
            s.pop()
        self.i.add_builtin('play-note', _play_note)
        self.assertEqual(self.i.interpret("(66 play-note)"), [])
        # major-chord = dup play-note 5 + dup play-note 7 + play-note
        self.assertEqual(self.i.interpret("(66 (dup play-note 5 + dup play-note 7 + play-note) eval)"), [])

if __name__ == '__main__':
    unittest.main()
