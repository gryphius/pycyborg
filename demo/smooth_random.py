#!/usr/bin/env python

"""Smooth random transitions demo"""
import random
import sys
import time
sys.path.insert(0,'../')

from pycyborg import get_all_cyborgs

def _random_rgb():
    return random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)

def _approach(current, target):
    if current < target:
        return current + 1
    elif current > target:
        return current - 1
    else:
        return current

def _approach_rgb(r, g, b, r_target, g_target, b_target):
    return _approach(r, r_target), _approach(g, g_target), _approach(b, b_target),


cyborgs=get_all_cyborgs()
numcyborgs=len(cyborgs)
if numcyborgs==0:
    print("no cyborg gaming lights found :(")
    sys.exit(1)

red, green, blue = _random_rgb()

try:
    while numcyborgs>0:
        red_target, blue_target, green_target = _random_rgb()
        while red != red_target and blue != blue_target and green != blue_target:
            red, green, blue = _approach_rgb(red, green, blue, red_target, green_target, blue_target)
            for cyborgindex in range(numcyborgs):
                cyborgs[cyborgindex].set_rgb_color(red,green,blue)
            time.sleep(.45)

except KeyboardInterrupt:
    pass

for cyborg in cyborgs:
    cyborg.set_rgb_color(0,0,0)
