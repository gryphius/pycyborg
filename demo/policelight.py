#!/usr/bin/env python

"""Red/Blue flashing lights demo"""

import sys
sys.path.insert(0,'../')

from pycyborg import get_all_cyborgs

cyborgs=get_all_cyborgs()
numcyborgs=len(cyborgs)
if numcyborgs==0:
    print "no cyborg gaming lights found :("
    sys.exit(1)

green=0
try:
    while numcyborgs>0:
        for colorval in range(255):
            for cyborgindex in range(numcyborgs):
                
                if (cyborgindex+1)%2==0:
                    red=colorval
                    blue=255-colorval
                else:
                    red=255-colorval
                    blue=colorval
                
                cyborgs[cyborgindex].set_rgb_color(red,green,blue)    
                
        for colorval in range(255):
            colorval=255-colorval
            for cyborgindex in range(numcyborgs):
                
                if (cyborgindex+1)%2==0:
                    red=colorval
                    blue=255-colorval
                else:
                    red=255-colorval
                    blue=colorval
                
                cyborgs[cyborgindex].set_rgb_color(red,green,blue)

    
except KeyboardInterrupt:
    pass

for cyborg in cyborgs:
    cyborg.set_rgb_color(0,0,0)
