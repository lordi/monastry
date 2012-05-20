python << endpython
import time
import os
from threading import Thread, Lock
import vim
import scosc

# Remember that the vim object is not threadsafe.

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
            b.pc += 1
            if b.pc > len(b.buffer):
                b.pc = 1
            b.interpret(b.buffer[b.pc - 1])

    def add_buffer(self):
        print "add buffer:", vim.current.buffer.name
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
        print "called exit."
        self.alive = False
        self.lock.release()

mot = Monastry()
mot.start()
endpython

function! MyCoolFunction()
python << endpython
mot.update_vim()
vim.command("return 1")
endpython
endfunction

function! ShouldIReallyExit()
python << endpython
mot.exit()
endpython
    qall
endfunction

function! Timer()
  call feedkeys("f\e") " this needs some tweaking because C-W does not work reliably anymore
python << endpython
mot.update_vim()
endpython
endfunction

sign define pc text=> texthl=Search

augroup vimcollider
    au CursorHold * call Timer()
    " TODO: insert mode autocmd CursorHoldI * call Timer()
    au BufRead *.mot py mot.add_buffer()
    au VimLeavePre * call ShouldIReallyExit() 
augroup END

set updatetime=100

