import scosc
import os
from subprocess import call
from base import MonastryBackend

class SuperColliderBackend (MonastryBackend):
    def __init__(self):
        pass

    def start(self, monastry):
        self.server = scosc.Controller(("localhost", 57110),verbose=True)
        call(['sclang', os.path.expanduser(\
                "~/.vim/bundle/monastry/mots/init.sc")])

        monastry.interpreter.add_builtin('play-note', self._play_note)

    def _play_note(self, stack):
        freq = int(s.pop())

