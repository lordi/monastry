python << endpython

import vim
import thread
import time
from threading import Thread, Lock

# Remember that the vim object is not threadsafe.
class VimCollider(Thread):
    vc_buffers = []
    vc_exit = False
    vc_data_lck = Lock()

    def run(self):
        self.vc_data_lck.acquire()
        while not self.vc_exit:
            self.vc_data_lck.release()
            time.sleep(0.2)
            self.vc_data_lck.acquire()
            self.step()
        self.vc_data_lck.release()

    def step(self):
        for b in self.vc_buffers:
            b['pc'] += 1
            if b['pc'] > len(b['buffer']):
                b['pc'] = 1

    def add_buffer(self):
        print "add buffer:", vim.current.buffer.name
        self.vc_buffers.append({'pc': 1, 'prev_pc': 1, 'buffer': vim.current.buffer})

    def update_vim(self):
        self.vc_data_lck.acquire()
        #vim.current.buffer.append("pc=%d at %s" % (vc_data['pc'], time.ctime(time.time()) ))
        #print vc_data
        for b in self.vc_buffers:
            vim.command(":sign place {0} line={0} name=pc file={1}".format(b['pc'], b['buffer'].name))
            if b['prev_pc'] != b['pc']:
                vim.command(":sign unplace {0}".format(b['prev_pc']))
                b['prev_pc'] = b['pc']
        self.vc_data_lck.release()

    def exit(self):
        print "called exit.", vc_exit
        self.vc_data_lck.acquire()
        vc_exit = True
        self.vc_data_lck.release()

vc = VimCollider()
vc.start()
endpython

function! MyCoolFunction2()
python << endpython
#vc.update_vim()
endpython
endfunction

function! MyCoolFunction()
python << endpython
vc.update_vim()
vim.command("return 1")
endpython
endfunction

function! ShouldIReallyExit()
python << endpython
vc.exit()
endpython
    qall
endfunction

function! Timer()
  call feedkeys("f\e")
  "let lastline = line("w$")
  "let recent = g:vc_pc
  "let g:vc_pc = g:vc_pc >= lastline ? 1 : g:vc_pc + 1
python << endpython
vc.update_vim()
endpython
  "  :exe ":sign place " . g:vc_pc . " line=" . g:vc_pc . " name=pc file=" . expand("%:p")
  ":exe ":sign unplace " . recent
  " K_IGNORE keycode does not work after version 7.2.025)
  " there are numerous other keysequences that you can use
endfunction

sign define pc text=> texthl=Search

augroup vimcollider
    au CursorHold * call Timer()
    " TODO: insert mode autocmd CursorHoldI * call Timer()
    au BufRead *.vc py vc.add_buffer()
    "au VimLeavePre * call ShouldIReallyExit() 
augroup END

set updatetime=100

