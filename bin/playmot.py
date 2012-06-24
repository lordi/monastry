"""
Command line tool to play Monastry files without vim
"""
import sys
import time

from monastry import Monastry
from monastry.backends import SuperColliderBackend
from monastry.track import LinesTrack

if len(sys.argv) != 2:
    print __doc__
    print "Usage: {0} <motfile>".format(sys.argv[0])
    exit(1)

inputlines = file(sys.argv[1]).readlines()
mot = Monastry(SuperColliderBackend())
mot.bpm = 120
mot.steps = 4
mot.add_track(LinesTrack(mot, inputlines))
mot.start()
time.sleep(10.0)
mot.exit()
del mot
time.sleep(0.1)

