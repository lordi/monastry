from pyparsing import *

class Interpreter:
    def _1ary(func): return lambda s: s.append(func(s.pop()))
    def _2ary(func): return lambda s: s.append(func(s.pop(), s.pop()))
    def _3ary(func): return lambda s: s.append(func(s.pop(), s.pop(), s.pop()))
    def _swap(s): top = s.pop(); snd = s.pop(); s.append(top); s.append(snd)
    def _combine(s):
        elem = s.pop()
        lst = []
        while elem != '[':
            lst.append('eval')
            lst.append(elem)
            elem = s.pop()
        lst.reverse()
        s.append(lst)

    builtins = {
            'inc':  _1ary(lambda x: x + 1),
            'dec':  _1ary(lambda x: x - 1),

            'wrap':  _1ary(lambda x: [x]),
            'wrap2': _2ary(lambda x, y: [y, x]),
            'wrap3': _3ary(lambda x, y, z: [z, y, x]),

            '+':    _2ary(lambda x, y: y + x),
            '-':    _2ary(lambda x, y: y - x),
            'mul':  _2ary(lambda x, y: y * x),
            'div':  _2ary(lambda x, y: int(y // x)),
            'mod':  _2ary(lambda x, y: int(y % x)),
            'eq':   _2ary(lambda x, y: 1 if x == y else 0),
            'lt':   _2ary(lambda x, y: 1 if y < x else 0),
            ']':    _combine,
            'dup':  lambda s: s.append(s[-1]),
            'drop': lambda s: s.pop(),
            'swap': _swap
    }

    aliases = {
            # delay function f by t steps
            # <f> <t> delay := (wrap) swap dec times
            'delay': [['wrap'], 'swap', 'dec', 'times'],
    }

    def __init__(self):
        pass

    def add_builtin(self, name, func):
        """

        Add a builtin function:

        @param func a function that recieves a stack to manipulate
        """
        self.builtins[name] = func

    def set_alias(self, name, tree):
        """

        Add an alias

        """
        assert type(tree) == list, "alias replacement must be list"
        self.aliases[name] = tree

    def reduce_item(self, item, stack):
        try:
            if type(item) == str:
                item = int(item)
        except ValueError:
            pass
        if type(item) == str and self.builtins.has_key(item):
            self.builtins.get(item)(stack)
        elif type(item) == str and self.aliases.has_key(item):
            tree = self.aliases.get(item)
            stack = self.reduce(tree, stack)
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

