#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.info('Started')
from pycyborg import get_all_cyborgs

if __name__ == '__main__':
    cyborgs=get_all_cyborgs()
    print("found and initialized %s cyborg ambx gaming lights"%(len(cyborgs)))
    if len(cyborgs)!=0:
        logging.info('Using %s',cyborgs[0].usbdev.backend.__module__)
            
    counter=0
    for cy in cyborgs:
        counter+=1
        print("Cyborg %s: "%counter)
        print(cy)
        cy.set_intensity(50)
        cy.set_rgb_color(255,255,255)
        cy.transition_to(255,0,0,duration=0.3)
        cy.transition_to(0,255,0,duration=0.3)
        cy.transition_to(0,0,255,duration=0.3)
        cy.transition_to(0,0,0,duration=0.3)
        print("")
        
