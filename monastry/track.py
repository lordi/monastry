# A track is a buffer.
class Track:
    def __init__(self, monastry):
        self.pc = 1
        self.prev_pc = 1
        self.synth = 'wobble'
        self.monastry = monastry
        import random
        self.id = random.randint(1000,2000)
        self.stack = []

    def step(self):
        if self.pc > len(self.buffer):
            self.pc = 1
        curr_pc = self.pc
        self.pc += 1
        if self.pc > len(self.buffer):
            self.pc = 1
        while len(self.buffer[self.pc - 1]) > 0 and self.buffer[self.pc - 1][0] == '#' and self.pc != curr_pc:
            self.pc += 1
            if self.pc > len(self.buffer):
                self.pc = 1

    def interpret(self, line):
        newstack = []
        pcs = []
        def set_pc(s):
            pcs.append(s.pop())
        self.monastry.interpreter.set_alias('pc>', [self.pc])
        self.monastry.interpreter.add_builtin('>pc', set_pc)
        for term in self.stack:
            if type(term) == list:
                newstack = self.monastry.interpreter.reduce(term, newstack)
        self.stack = self.monastry.interpreter.interpret(line, newstack)
        if len(pcs) > 0:
            self.pc = pcs[-1]
        #print "> ", self.stack

class VimBufferTrack (Track):
    def __init__(self, monastry, buffer):
        self.buffer = buffer
        Track.__init__(self, monastry)

class LinesTrack (Track):
    def __init__(self, monastry, lines):
        self.buffer = lines
        Track.__init__(self, monastry)
        self.pc = 0
        self.prev_pc = 0

if __name__ == "__main__":
    import doctest
    doctest.testmod()
