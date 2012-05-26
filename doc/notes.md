Some links for development
--------------------------

 * http://brainacle.com/how-to-write-vim-plugins-with-python.html
 * https://trac.assembla.com/pkaudio/browser/bin/pkscmidi
 * Syndefs:
    * http://supercollider.tsd.net.au/SynthDefPool
    * http://sccode.org/tag/class/Synth

Language design
---------------

 * Terminology: Main class == Monastry, each buffer/track == Scripture?
 * Required functions:
    * program counter manipulation, jumps, e.g. "(jump -4)"
    * conditional jumps, cascaded loops, e.g. "(repeat 2 8)"
    * Multiple return values, e.g. "(major-triad D)"
    * filter envelopes, kinda running parallel to pc, e.g. "(for 4 (100 mul change \freq))"
 * Question:
    * Can vimL play a role in it?
    * New language? functional/concatenative?
    * With or without side effects?
    * Solvable with stacks or are registeres needed?


