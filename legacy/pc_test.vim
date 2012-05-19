" program counter
let g:vc_pc = 1
sign define pc text=> texthl=Search

augroup vimcollider
    autocmd CursorHold * call Timer()
    " TODO: insert mode autocmd CursorHoldI * call Timer()
augroup END

function! Timer()
  call feedkeys("f\e")
  let lastline = line("w$")
  let recent = g:vc_pc
  let g:vc_pc = g:vc_pc >= lastline ? 1 : g:vc_pc + 1
  :exe ":sign place " . g:vc_pc . " line=" . g:vc_pc . " name=pc file=" . expand("%:p")
  :exe ":sign unplace " . recent
  " K_IGNORE keycode does not work after version 7.2.025)
  " there are numerous other keysequences that you can use
endfunction

set updatetime=100
