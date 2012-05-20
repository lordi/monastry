class Track:
    def __init__(self, monastry, buffer):
        self.pc = 1
        self.prev_pc = 1
        self.buffer = buffer
        self.synth = 'wobble'
        self.monastry = monastry
        self.monastry.load_synth(self.synth)

    def interpret(self, line):
        notes = line.split(' ')
        i = 0
        for n in notes:
            try:
                osc = ('/s_new', self.synth, 1075+self.pc*100+i, 1, 0, 'freq', int(n)*100)
                self.monastry.server.sendMsg(*osc)
            except Exception:
                pass
            i = i + 1
