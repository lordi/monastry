from pyparsing import *

class Interpreter:
    def _1ary(func): return lambda s: s.append(func(s.pop()))
    def _2ary(func): return lambda s: s.append(func(s.pop(), s.pop()))
    def _swap(s): top = s.pop(); snd = s.pop(); s.append(top); s.append(snd)

    builtins = {
            'inc':  _1ary(lambda x: x + 1),
            'dec':  _1ary(lambda x: x - 1),
            'wrap': _1ary(lambda x: [x]),

            '+':    _2ary(lambda x, y: y + x),
            '-':    _2ary(lambda x, y: y - x),
            'mul':  _2ary(lambda x, y: y * x),
            'div':  _2ary(lambda x, y: int(y // x)),
            'mod':  _2ary(lambda x, y: int(y % x)),
            'eq':   _2ary(lambda x, y: 1 if x == y else 0),
            'lt':   _2ary(lambda x, y: 1 if y < x else 0),
            'dup':  lambda s: s.append(s[-1]),
            'drop': lambda s: s.pop(),
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
        try:
            if type(item) == str:
                item = int(item)
        except ValueError:
            pass
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
        # TODO convert ints during
        nestedItems = nestedExpr()
        return nestedItems.parseString("({0})".format(data)).asList().pop()

    def interpret(self, data, stack = None):
        if stack == None: stack = []
        for tree in self.scan(data):
            if type(tree) == list:
                stack = self.reduce(tree, stack)
        return stack

