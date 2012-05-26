python << endpython
import sys
import os
import logging

logging.basicConfig(filename='monstry.log', level=logging.INFO)
logging.info('Started')

# TODO fix imports
sys.path.append('.')
sys.path.append(os.path.expanduser('~/.vim/bundle/monastry'))
sys.path.append('../monastry')

mot = None
try:
    from monastry import Monastry
    mot = Monastry()
    mot.start()
except e:
    logging.exception(e)
endpython

function! MonastryUpdate()
    py if mot: mot.update_vim()
endfunction

function! MonastryExit()
    py logging.info('Requested finish')
    py if mot: mot.exit()
    qall
endfunction

function! MonastryTimer()
    call feedkeys("f\e") " this needs some tweaking because C-W does not work reliably anymore
    call MonastryUpdate()
endfunction

sign define pc text=> texthl=Search
set updatetime=100

augroup vimcollider
    au CursorHold * call MonastryTimer()
    " TODO: insert mode autocmd CursorHoldI * call Timer()
    au BufRead *.mot py if mot: mot.add_buffer()
    au VimLeavePre * call MonastryExit() 
augroup END
