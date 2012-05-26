import sys
import os
import time
import atexit
from monastry import Monastry, LinesTrack

mot = Monastry()
mot.start()
atexit.register(mot.exit)
try:
    mot.add_track(LinesTrack(mot, ['(synth "mario") *1', '*2', '',  '', '*3', '*4', '', '']))
    mot.add_track(LinesTrack(mot, ['(synth "bass") ', '*2', ' ', '*4']))
    mot.add_track(LinesTrack(mot, ['(synth "beat") *1', '', '*3', '']))
    time.sleep(10)
except Exception, e:
    print e
finally:
    mot.exit()


