import time
import os
from threading import Thread, Lock
import logging
from track import Track
from interpret import Interpreter

class MonastryBackend:
    def __init__(self):
        pass

    def start(self, monastry):
        pass

    def stop(self):
        pass

class Monastry(Thread):
    tracks = []
    alive = True
    backend = None
    bpm = 120 # beats per minute
    spb = 4   # steps per beats
    steps = 0   # exit after this number of steps if gt 0

    def __init__(self, backend):
        self.backend = backend
        self.interpreter = Interpreter()
        self.tracks = []
        self.lock = Lock()
        Thread.__init__(self)

    def run(self):
        self.lock.acquire()
        self.backend.start(self)
        while self.alive:
            self.lock.release()
            if self.bpm > 0 and self.spb > 0:
                time.sleep(60.0/self.bpm/self.spb)
            self.lock.acquire()
            try:
                self.step()
            except Exception, e:
                print e
                self.alive = False
        self.lock.release()

    def step(self):
        for b in self.tracks:
            b.step()
            b.interpret(b.buffer[b.pc - 1])
        if self.steps > 0:
            if self.steps == 1:
                self.alive = False
            self.steps -= 1

    def add_track(self, track):
        self.tracks.append(track)

    def add_buffer(self):
        " Add current vim buffer as a track "
        import vim
        self.add_track(VimBufferTrack(self, vim.current.buffer))

    def update_vim(self):
        import vim
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

