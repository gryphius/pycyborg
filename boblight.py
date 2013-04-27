#!/usr/bin/python2

"""
Boblight interface for pycyborg
"""


import sys


while True:
    line=sys.stdin.readline().strip()
    colors = line.split()
    numchannels=len(colors)
    if numchannels%3!=0:
        sys.stderr.write("Expecting 3 channels per device. got %s - check boblight.conf ! \n"%numchannels)
        continue
    
    numdevices=numchannels/3
    print "numdevices=%s"%numdevices
    
    
    
    print colors
