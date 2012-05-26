Some links for development
--------------------------

 * http://brainacle.com/how-to-write-vim-plugins-with-python.html
 * https://trac.assembla.com/pkaudio/browser/bin/pkscmidi
 * Syndefs:
    * http://supercollider.tsd.net.au/SynthDefPool
    * http://sccode.org/tag/class/Synth

Language design
---------------

 * Terminology
   * Main class == Monastry
   * each buffer/script file == Scripture
   * each track (interpreting the buffer) == Meditation (following Scripture)
 * Required functions:
    * program counter manipulation, jumps, e.g. `(jump -4)`
    * conditional jumps, cascaded loops, e.g. `(repeat 2 8)`
    * Multiple return values, e.g. `(major-triad D)`
   *  filter envelopes, kinda running parallel to pc, e.g. `(next-n 4 (dup 100 mul freq set))`
 * Question:
    * Can vimL play a role in it?
    * New language? functional/concatenative?
    * With or without side effects?
    * Solvable with stacks or are registeres needed?


