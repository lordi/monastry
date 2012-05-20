Monastry - supercollider tracker with vim interface
===================================================

This does not function yet, work in progress.

Run proof of concept
--------------------

    SC_JACK_DEFAULT_OUTPUTS="system:playback_1,system:playback_2" scsynth -u 57110
    vim --cmd ':so monastry.vim' patterns/pattern.mot

Some notes
----------

 * http://brainacle.com/how-to-write-vim-plugins-with-python.html
 * https://trac.assembla.com/pkaudio/browser/bin/pkscmidi
 * Terminology: Main class == Monastry, each buffer == Scripture?


