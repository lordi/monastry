python << endpython
import time
import os
from threading import Thread, Lock
import vim
import scosc

# Remember that the vim object is not threadsafe.
class Monastry(Thread):
    buffers = []
    alive = True
    lock = Lock()

    def run(self):
        server = scosc.Controller(("localhost", 57110),verbose=True)
        fpath = '~/src/monastry/sound/synths/wobble.scsyndef'
        server.sendMsg('/d_load', os.path.expanduser(fpath))
        osc = ('/s_new', 'wobble', 1075, 1, 0, 'key', 0)
        self.server = server
        time.sleep(1)
        self.server.sendMsg(*osc)
        print '<<<', osc

        print server
        #options.host, int(options.port)),
        #                      verbose=options.verbose,
        #                      spew=options.spew)

        self.lock.acquire()
        while self.alive:
            self.lock.release()
            time.sleep(0.2)
            self.lock.acquire()
            self.step()
        self.lock.release()

    def step(self):
        for b in self.buffers:
            b['pc'] += 1
            if b['pc'] > len(b['buffer']):
                b['pc'] = 1
            if b['buffer'][b['pc']-1].find('beat') >= 0:
                osc = ('/s_new', 'wobble', 1075+b['pc'], 1, 0)
                self.server.sendMsg(*osc)


    def add_buffer(self):
        print "add buffer:", vim.current.buffer.name
        self.buffers.append({'pc': 1, 'prev_pc': 1, 'buffer': vim.current.buffer})

    def update_vim(self):
        self.lock.acquire()
        #vim.current.buffer.append("pc=%d at %s" % (data['pc'], time.ctime(time.time()) ))
        #print data
        for b in self.buffers:
            vim.command(":sign place {0} line={0} name=pc file={1}".format(b['pc'], b['buffer'].name))
            if b['prev_pc'] != b['pc']:
                vim.command(":sign unplace {0}".format(b['prev_pc']))
                b['prev_pc'] = b['pc']
        self.lock.release()

    def exit(self):
        print "called exit."
        self.lock.acquire()
        alive = False
        self.lock.release()

mot = Monastry()
mot.start()
time.sleep(5)
endpython

function! MyCoolFunction2()
python << endpython
#mot.update_vim()
endpython
endfunction

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
    "au VimLeavePre * call ShouldIReallyExit() 
augroup END

set updatetime=100

