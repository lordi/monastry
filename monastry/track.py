class Track:
    def __init__(self, monastry, buffer):
        self.pc = 1
        self.prev_pc = 1
        self.buffer = buffer
        self.synth = 'wobble'
        self.monastry = monastry
        self.monastry.load_synth(self.synth)

    def interpret(self, line):
        if line.find('beat') >= 0:
            osc = ('/s_new', self.synth, 1075+self.pc, 1, 0)
            self.monastry.server.sendMsg(*osc)
