Monastry - supercollider tracker with vim interface
===================================================

This does not function yet, work in progress.

The goal of this project is to create a audio tracker with vim. This will include 
both a low-level step-oriented tracker language and a plugin that turns vim into 
a music production studio with [live coding](http://en.wikipedia.org/wiki/Live_coding)
capabilities.

Run proof of concept
--------------------

    SC_JACK_DEFAULT_OUTPUTS="system:playback_1,system:playback_2" scsynth -u 57110
    vim --cmd ':so monastry.vim' mots/new.mot

Some notes
----------

 * http://brainacle.com/how-to-write-vim-plugins-with-python.html
 * https://trac.assembla.com/pkaudio/browser/bin/pkscmidi
 * Terminology: Main class == Monastry, each buffer == Scripture?


