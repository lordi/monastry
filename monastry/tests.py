import unittest
from interpret import Interpreter
from monastry import Monastry, MonastryBackend
from track import LinesTrack
import time

class TestMonastry(unittest.TestCase):
    class TestBackend(MonastryBackend):
        def start(self, monastry):
            self.output = []
            def _print(s):
                self.output.append(s.pop())
            monastry.interpreter.add_builtin('print', _print)

    def assertOutput(self, input, output):
        be = TestMonastry.TestBackend()
        mot = Monastry(be)
        mot.bpm = -1
        mot.steps = len(input)
        mot.add_track(LinesTrack(mot, input))
        mot.start()
        time.sleep(0.1)
        mot.exit()
        del mot
        time.sleep(0.1)
        self.assertEqual(be.output, output)

    def test_combine_operator(self):
        self.assertOutput([
            '(6 print)',
            '( [ (7) (print) ] eval )',
            '( [ [ (pc>) (print) ] wrap (eval) ] eval)',
            ''
            ], [6, 7, 3])

    def test_jump(self):
        self.assertOutput([
            '',                     # 1
            '',                     # 2
            '(B print) (5 jump)',   # 3
            '(C print)',            # 4
            '(D print)',            # 5
            '(E print)',            # 6
            '',                     # 7
            ''
            ], ['B', 'D', 'E'])

        # endless loop with relative jump
        self.assertOutput([
            '(Z print)',
            '(A print)',
            '(B print)',
            '(2 jump-back)',
            '(C print)',
            '',
            '',
            '',
            ''
            ], ['Z', 'A', 'B', 'A', 'B', 'A', 'B'])


    def test_linestrack(self):
        self.assertOutput([
            '(6 print)',
            '',
            ''
            ], [6])

        self.assertOutput([
            '',
            ''
            ], [])

        self.assertOutput([
            '(pc> print)',
            '(pc> print)'
            ], [1, 2])

    def test_delay(self):
        self.assertOutput([
            '(pc> print) ((pc> print) 2 delay)',
            '',
            '',
            '',
            ], [1, 3])

        self.assertOutput([
            '( 2 [ pc> wrap (print) ] 3 delay )',
            '',
            '( pc> print )',
            '',
            ], [3, 1])

    def test_countdown(self):
        self.assertOutput(
            ['((print) 4 countdown)', '', '', '', '', '', ''],
            [4, 3, 2, 1])

        self.assertOutput(
            ['((square print) 4 countdown)', '', '', '', '', ''],
            [16, 9, 4, 1])

        self.assertOutput(
            [   '((square print) 4 countdown) ((100 mul print) 4 countdown)',
                '',
                '(666 print)',
                '',
                '',
                ''  ],
            [16, 400, 9, 300, 4, 200, 666, 1, 100])

    def test_sawtooth(self):
        # sawtooth
        self.assertOutput(
            ['((0 swap - 4 mod print) 12 countdown)', '', '', '',
                '', '', '', '',
                '', '', '', '', ''],
           [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3])

    def test_loop(self):
        self.assertOutput(
            ['(4 3 repeat)',
                '(A print)',
                '(B print)',
                '(C print)',
                '(D print)',
                '(E print)',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '',
                '' ],
           ['A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D',
               'A', 'B', 'C', 'D',
               'E'])
       
    def test_cplx(self):
        self.assertOutput([
            '(6 print)',
            '(6 2 + print)',
            '(6 2 mul print)',
            '(12 wrap) (13)',
            '(2 +) (print)',
            ], [6, 8, 12, 14])

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.i = Interpreter()

    def test_parenthesis(self):
        self.assertEqual(self.i.interpret(""), [])
        self.assertEqual(self.i.interpret("()"), [])
        self.assertEqual(self.i.interpret("(4)"), [4])
        self.assertEqual(self.i.interpret("(4 2)"), [4, 2])
        self.assertEqual(self.i.interpret("(4) (6) (+)"), [10])

    def test_arithmetic(self):
        self.assertEqual(self.i.interpret("(4 2 +)"), [6])
        self.assertEqual(self.i.interpret("(4 2 -)"), [2])
        self.assertEqual(self.i.interpret("(5 inc)"), [6])
        self.assertEqual(self.i.interpret("(7 dec)"), [6])
        self.assertEqual(self.i.interpret("(6 4 mod)"), [2])

    def test_infix(self):
        self.assertEqual(self.i.interpret("(6 (+) 2 swap eval)"), [8])

    def test_eval(self):
        self.assertEqual(self.i.interpret("(5 (inc) eval)"), [6])
        self.assertEqual(self.i.interpret("(21 (inc dec) eval)"), [21])

    def test_wrap(self):
        self.assertEqual(self.i.interpret("(2 wrap eval)"), [2])
        self.assertEqual(self.i.interpret("((5 inc) wrap eval eval)"), [6])
        self.assertEqual(self.i.interpret("(2 4 wrap2 eval)"), [2, 4])
        self.assertEqual(self.i.interpret("(1 2 3 4 wrap3)"), [1, [2, 3, 4]])
        self.assertEqual(self.i.interpret("(1 1 1 2 (inc) eval wrap2 eval)"), [1,1,1,3])

    def test_times(self):
        self.assertEqual(self.i.interpret("(4 (2 +) 3 times)"), [10])
        self.assertEqual(self.i.interpret("(13 (inc) 5 times 2 +)"), [20])

    def test_if(self):
        self.assertEqual(self.i.interpret("(1 5 lt)"), [1])
        self.assertEqual(self.i.interpret("(1 5 gt)"), [0])
        self.assertEqual(self.i.interpret("(1 5 eq)"), [0])
        self.assertEqual(self.i.interpret("(5 5 eq)"), [1])
        self.assertEqual(self.i.interpret("(5 5 gt)"), [0])
        self.assertEqual(self.i.interpret("(5 5 gte)"), [1])

        self.assertEqual(self.i.interpret("(20 1 (10 +) if)"), [30])
        self.assertEqual(self.i.interpret("(20 0 (10 +) if)"), [20])

        # inc-lt50 = dup 50 lt (inc) if
        self.assertEqual(self.i.interpret("(45 (dup 50 lt (inc) if) eval)"), [46])
        self.assertEqual(self.i.interpret("(50 (dup 50 lt (inc) if) eval)"), [50])
        self.assertEqual(self.i.interpret("(45 (dup 50 lt (inc) if) 10 times)"), [50])

    def test_swap(self):
        self.assertEqual(self.i.interpret("(10 12 swap lt)"), [0])
        self.assertEqual(self.i.interpret("(50 (inc) swap swap eval)"), [51])

    def test_default_stack(self):
        self.assertEqual(self.i.interpret("(4 +)", [20]), [24])
        self.assertEqual(self.i.interpret("(4 swap eval)", [20, '+']), [24])

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
