import time
import os
from threading import Thread, Lock
import vim
import scosc
from track import Track

class Monastry(Thread):
    tracks = []
    alive = True
    lock = Lock()

    def run(self):
        self.server = scosc.Controller(("localhost", 57110),verbose=True)
        self.lock.acquire()
        while self.alive:
            self.lock.release()
            time.sleep(0.2)
            self.lock.acquire()
            self.step()
        self.lock.release()

    def load_synth(self, name):
        fpath = '~/src/monastry/sound/synths/{0}.scsyndef'.format(name)
        self.server.sendMsg('/d_load', os.path.expanduser(fpath))

    def step(self):
        for b in self.tracks:
            b.step()
            b.interpret(b.buffer[b.pc - 1])

    def add_buffer(self):
        self.tracks.append(Track(self, vim.current.buffer))

    def update_vim(self):
        self.lock.acquire()
        #vim.current.buffer.append("pc=%d at %s" % (data['pc'], time.ctime(time.time()) ))
        #print data
        for b in self.tracks:
            vim.command(":sign place {0} line={0} name=pc file={1}".format(b.pc, b.buffer.name))
            if b.prev_pc != b.pc:
                vim.command(":sign unplace {0}".format(b.prev_pc))
                b.prev_pc = b.pc
        self.lock.release()

    def exit(self):
        self.lock.acquire()
        self.alive = False
        self.lock.release()

