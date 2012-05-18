python << endpython

import vim
import thread
import time
from threading import Thread, Lock

vc_data = {'pc': 0, 'exit': False} 
vc_data_lck = Lock()

# Remember that the vim object is not threadsafe.
class VimCollider(Thread):
    def run(self):
        self.pc = 0
        vc_data_lck.acquire()
        while not vc_data['exit']:
            vc_data_lck.release()
            time.sleep(1)
            vc_data_lck.acquire()
            vc_data['pc'] += 1
        vc_data_lck.release()

    def update_vim(self):
        vc_data_lck.acquire()
        vim.current.buffer.append("pc=%d at %s" % (vc_data['pc'], time.ctime(time.time()) ))
        vc_data_lck.release()

    def exit(self):
        vc_data_lck.acquire()
        vc_data['exit'] = True
        vc_data_lck.release()

vc = VimCollider()
vc.start()
endpython

function! MyCoolFunction()
python << endpython
vc.update_vim()
endpython
endfunction

function! ShouldIReallyExit()
python << endpython
vc.exit()
endpython
    qall
endfunction

au VimLeavePre * call ShouldIReallyExit() 
