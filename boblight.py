#!/usr/bin/env python

"""
Boblight interface for pycyborg
"""

import sys
from pycyborg import get_all_cyborgs

cyborgs=get_all_cyborgs()

for cy in cyborgs:
    cy.set_intensity(50)

warn_wrong_channel_count=True

while True:
    try:
        line=sys.stdin.readline().strip()
    except:
        break
    colors = line.split()
    numchannels=len(colors)
    if numchannels%3!=0:
        sys.stderr.write("Expecting 3 channels per device. got %s - check boblight.conf ! \n"%numchannels)
        continue
    
    numdevices=numchannels/3
    if warn_wrong_channel_count and numdevices!=len(cyborgs):
        sys.stderr.write("WARNING: I found %s cyborgs but boblights sends data for %s devices !"%(len(cyborgs),numdevices))
        warn_wrong_channel_count=False
    
    
    for n in range(numdevices):
        floatlist=colors[n*3:n*3+3]
        intlist=[int(round(float(x)*256)) for x in floatlist]
        cyborgs[n].set_rgb_color(intlist[0],intlist[1],intlist[2])


for cy in cyborgs:
    cy.lights_off()
