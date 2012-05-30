from pyparsing import *
import pprint

def reduce_item(item, stack):
    if item == '+':
        stack.append(int(stack.pop())+int(stack.pop()))
    elif item == 'dup':
        item = stack.pop()
        stack.append(item)
        stack.append(item)
    elif item == 'swap':
        top = stack.pop()
        snd = stack.pop()
        stack.append(top)
        stack.append(snd)
    elif item == 'eq':
        stack.append(1 if int(stack.pop()) == int(stack.pop()) else 0)
    elif item == 'lt':
        stack.append(1 if int(stack.pop()) > int(stack.pop()) else 0)
    elif item == 'if':
        func = stack.pop()
        if int(stack.pop()) == 1: stack = reduce(func, stack)
    elif item == 'inc':
        stack.append(int(stack.pop())+1)
    elif item == 'times':
        times = int(stack.pop())
        insert = stack.pop()
        for i in range(times):
            stack.append(insert)
            stack = reduce_item('eval', stack) 
    elif item == 'eval':
        stack = reduce(stack.pop(), stack)
    else:
        stack.append(item)
    return stack

def reduce(tree, stack=None):
    if stack == None: stack = []; print "-" * 40
    print "Reducing", tree
    for elem in tree:
        stack = reduce_item(elem, stack)
        print elem, "=>", stack
    return stack

def scan(data):
    nestedItems = nestedExpr()
    return nestedItems.parseString(data).asList().pop()

def interpret(data):
    print scan(data)
    return reduce(scan(data))


import unittest

class TestSequenceFunctions(unittest.TestCase):
    def test_xxx(self):
        self.assertEqual(interpret("(2 4 +)"), [6])
        self.assertEqual(interpret("(5 inc)"), [6])
        self.assertEqual(interpret("(5 (inc) eval)"), [6])
        self.assertEqual(interpret("(4 (2 +) 3 times)"), [10])
        self.assertEqual(interpret("(13 (inc) 5 times 2 +)"), [20])

    def test_increase_only_if_lt_50(self): # inc-lt50 = dup 50 lt (inc) if
        self.assertEqual(interpret("(45 (dup 50 lt (inc) if) eval)"), [46])
        self.assertEqual(interpret("(50 (dup 50 lt (inc) if) eval)"), ['50'])
        self.assertEqual(interpret("(45 (dup 50 lt (inc) if) 10 times)"), [50])

    def test_swap(self):
        self.assertEqual(interpret("(10 12 swap lt)"), [0])
        self.assertEqual(interpret("(50 (inc) swap swap eval)"), [51])

if __name__ == '__main__':
    unittest.main()
