import time
import scosc
import os

id = 4000
synthdef = 'wobble'
server = scosc.Controller(("localhost", 57110),verbose=True)
fpath = '~/src/monastry/sound/synths/{0}.scsyndef'.format(synthdef)
server.sendMsg('/status')
if not os.path.exists(os.path.expanduser(fpath)):
    exit(1)
server.sendMsg('/d_load', os.path.expanduser(fpath))
time.sleep(1)
server.sendMsg('/status')
for i in range(id,id+10):
    osc = ('/s_new', synthdef, i, 1, 0) #, 'freq', 600)
    print '<<<', osc
    server.sendMsg(*osc)
    server.sendMsg('/status')
    time.sleep(0.15)

time.sleep(1)
