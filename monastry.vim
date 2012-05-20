python << endpython
from monastry import Monastry
import sys
mot = Monastry()
mot.start()
endpython

function! MonastryUpdate()
    py mot.update_vim()
endfunction

function! MonastryExit()
    py mot.exit()
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
    au BufRead *.mot py mot.add_buffer()
    au VimLeavePre * call MonastryExit() 
augroup END
