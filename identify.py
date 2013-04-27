#!/usr/bin/python2

from pycyborg import get_all_cyborgs
import time

if __name__ == '__main__':
    cyborgs=get_all_cyborgs()
    print "found and initialized %s cyborg gaming lights"%(len(cyborgs))
    print ""
    
    counter=0
    for cy in cyborgs:
        counter+=1
        print "Cyborg %s: "%counter
        print cy
        cy.set_intensity(50)
        cy.set_rgb_color(255,255,255)
        time.sleep(2)
        cy.lights_off()
        print ""
        
