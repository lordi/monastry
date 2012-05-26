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
    * program counter manipulation, jumps, e.g. `(-4 jump)`
    * conditional jumps, cascaded loops, e.g. `(2 8 repeat)`
    * Multiple return values, e.g. `("D" major-triad)`
    * filter envelopes, kinda running parallel to pc
    * something like lambda functions:
      * `(next-n 4 (100 mul "freq" set))` should be equivalent to:
        * `(0 100 mul "freq" set)`
        * `(1 100 mul "freq" set)`
        * `(2 100 mul "freq" set)`
        * `(3 100 mul "freq" set)`
      * before each of the consecutive lines
 * Question:
    * Can vimL play a role in it, e.g. `("gg" jump)` (probably not)
    * New language? functional/concatenative?
    * With or without side effects?
    * Solvable with stacks or are registeres needed?


