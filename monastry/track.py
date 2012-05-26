
# A track is a buffer.
class Track:
    def __init__(self, monastry):
        self.pc = 1
        self.prev_pc = 1
        self.synth = 'wobble'
        self.monastry = monastry
        import random
        self.i = random.randint(1000,2000)

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

    def parse(self, line):
        from sexp import parse
        if line.startswith('#'):
            return []
        else:
            return parse("({0})".format(line)).pop()

    def reduce(self, tree):
        #print tree, type(tree), len(tree)
        if type(tree) != tuple and type(tree) != list:
            return tree
        if len(tree) == 1:
            if (type(tree[0]) == str or type(tree[0]) == unicode):
                if tree[0][0] == '*':
                    return [["note-on"], int(tree[0][1:]) if len(tree[0]) > 1 else None]
                else:
                    return list(tree)
            elif type(tree[0]) == int:
                return []
        return map(self.reduce, tree)

    def parse_reduce(self, line):
        """
        >>> t = Track(None, None)
        >>> 
        >>> t.parse_reduce('*60')
        [[['note-on'], 60]]
        >>> 
        >>> t.parse_reduce('*62 *64')
        [[['note-on'], 62], [['note-on'], 64]]
        >>> 
        >>> t.parse_reduce('(synth "wobble") (vol 50) *66')
        [[['synth'], 'wobble'], [['vol'], 50], [['note-on'], 66]]
        >>>
        >>> t.parse_reduce('# Comment (synth wobble)')
        []
        >>> t.parse_reduce('       100')
        []
        >>> t.parse_reduce('')
        []
        """
        return self.reduce(self.parse(line))

    def interpret(self, line):
        commands = self.parse_reduce(line)
        for c in commands:
            try:
                cmd, args = c[0][0], c[1:]
                if cmd == "synth":
                    self.synth = args[0]
                elif cmd == "note-on":
                   self.i = self.i + 1
                   if args[0] != None:
                       osc = ('/s_new', self.synth, 1075+self.pc*100+self.i, 1, 0, 'freq', int(args[0])*100)
                   else:
                       osc = ('/s_new', self.synth, 1075+self.pc*100+self.i, 1, 0)
                   self.monastry.server.sendMsg(*osc)
            except Exception, e:
                print e

class VimBufferTrack (Track):
    def __init__(self, monastry, buffer):
        self.buffer = buffer


if __name__ == "__main__":
    import doctest
    doctest.testmod()
