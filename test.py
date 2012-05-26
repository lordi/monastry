import sys
import os
import time
from monastry import Monastry, Track

import atexit
#def cleanup():
#    mot.exit()
#if __name__ == "__main__":

class TestTrack (Track):
    def __init__(self, monastry, lines):
        self.buffer = lines
        Track.__init__(self, monastry)


mot = Monastry()

#grep_stdout = p.communicate(input=file('init.sc').read())
#input='''
#y = SynthDef("bass", { |out, amp=0.5, freq=440| var snd; snd = LFTri.ar(freq)!2; snd = snd * EnvGen.ar(Env.linen(0.001, 0.1, 0.53), doneAction:2); OffsetOut.ar(out, snd*amp); }).add;
#y.load(s)
#''')
#print(grep_stdout)

#input = StringIO.StringIO()
#input.write('xx\n')
#call("sclang", stdin=input)

mot.start()
atexit.register(mot.exit)
try:
    mot.add_track(TestTrack(mot, [ '', '(synth "mario") *1', '*2', '',  ]))
    mot.add_track(TestTrack(mot, [ '(synth "bass") ', '*2', ' ', '*4' ]))
    mot.add_track(TestTrack(mot, [ '(synth "beat") *1', '', '*3', '' ]))
    time.sleep(10)
except Exception, e:
    print e
finally:
    mot.exit()


