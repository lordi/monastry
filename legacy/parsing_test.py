from pyparsing import *
import pprint

# todo convert to int while scanning

def mk_1ary(func): return lambda s: s.append(func(s.pop()))
def mk_2ary(func): return lambda s: s.append(func(s.pop(), s.pop()))

class Interpreter:
    def _swap(s): top = s.pop(); snd = s.pop(); s.append(top); s.append(snd)

    builtins = {
            '+':    mk_2ary(lambda x, y: int(x) + int(y)),
            'inc':  mk_1ary(lambda x: int(x) + 1),
            'eq':   mk_2ary(lambda x, y: 1 if x == y else 0),
            'lt':   mk_2ary(lambda x, y: 1 if int(y) < int(x) else 0),
            'dup':  lambda s: s.append(s[-1]),
            'drop': lambda s: s.pop(),
            'wrap': mk_1ary(lambda x: [x]),
            'swap': _swap
    }

    def __init__(self):
        pass

    def add_builtin(self, name, func):
        """
        
        Add a builtin function:

        @param func a function that recieves a stack to manipulate
        """
        self.builtins[name] = func

    def reduce_item(self, item, stack):
        if type(item) == str and self.builtins.has_key(item):
            self.builtins.get(item)(stack)
        elif item == 'if':
            func = stack.pop()
            if int(stack.pop()) == 1: self.reduce(func, stack)
        elif item == 'times':
            times = int(stack.pop())
            insert = stack.pop()
            for i in range(times):
                stack.append(insert)
                self.reduce_item('eval', stack) 
        elif item == 'eval':
            stack = self.reduce(stack.pop(), stack)
        else:
            stack.append(item)

    def reduce(self, tree, stack=None):
        if stack == None: stack = []
        for elem in tree:
            #print stack, "<=", elem
            self.reduce_item(elem, stack)
            #print elem, "=>", stack
        return stack

    def scan(self, data):
        nestedItems = nestedExpr()
        return nestedItems.parseString(data).asList().pop()

    def interpret(self, data):
        return self.reduce(self.scan(data))

import unittest

class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.i = Interpreter()

    def test_eval(self):
        self.assertEqual(self.i.interpret("(2 4 +)"), [6])
        self.assertEqual(self.i.interpret("(5 inc)"), [6])
        self.assertEqual(self.i.interpret("(5 (inc) eval)"), [6])

    def test_wrap(self):
        self.assertEqual(self.i.interpret("(2 wrap eval)"), ['2'])
        self.assertEqual(self.i.interpret("((5 inc) wrap eval eval)"), [6])

    def test_times(self):
        self.assertEqual(self.i.interpret("(4 (2 +) 3 times)"), [10])
        self.assertEqual(self.i.interpret("(13 (inc) 5 times 2 +)"), [20])

    def test_if(self):
        self.assertEqual(self.i.interpret("(20 1 (10 +) if)"), [30])
        self.assertEqual(self.i.interpret("(20 0 (10 +) if)"), ['20'])

        # inc-lt50 = dup 50 lt (inc) if
        self.assertEqual(self.i.interpret("(45 (dup 50 lt (inc) if) eval)"), [46])
        self.assertEqual(self.i.interpret("(50 (dup 50 lt (inc) if) eval)"), ['50'])
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
