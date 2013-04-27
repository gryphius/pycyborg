#!/usr/bin/python

import usb.core
import time
import random
import sys

VENDOR=0x06a3
PRODUCT=0x0dc5
CONFIGURATION=1


def color(dev,r=0,g=0,b=0):
    """Set the light to a specific color"""
    r=int(r)
    g=int(g)
    b=int(b)
    dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a2, wIndex=0, data_or_wLength=[0xa2,0x00,r,g,b,0x00,0x00,0x00,0x00])
    
def transition(dev,target_r,target_g,target_b,duration=1,updatetime=0.001,start_r=0,start_g=0,start_b=0):
    """Transition from one color to another"""
    color(dev,start_r,start_g,start_b)
    starttime=time.time()
    steps=duration/updatetime
    
    step_r=(target_r-start_r)/steps
    step_g=(target_g-start_g)/steps
    step_b=(target_b-start_b)/steps
    for step in range(int(steps)):
        time.sleep(updatetime)
        new_r=start_r+(step*step_r)
        new_g=start_g+(step*step_g)
        new_b=start_b+(step*step_b)
        color(dev,new_r,new_g,new_b)
        
    color(dev,target_r,target_g,target_b)
    
def all_off(dev):
    """Turn off all lights"""
    color(dev,0,0,0)

def random_color():
    """Generate a random color tuple"""
    r=random.randint(0,255)
    g=random.randint(0,255)
    b=random.randint(0,255)
    return r,g,b

#find the first ambx madcatz gaming light
print "Searching for a madcatz ambx gaming light..."
dev=usb.core.find(idVendor=VENDOR,idProduct=PRODUCT)

if dev!=None:
    print "Found!"
else:
    print "Not found :( "
    sys.exit(1)

dev.set_configuration(CONFIGURATION)

#set idle request
dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x0a, wValue=0x00, wIndex=0, data_or_wLength=None)

#init
dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a7, wIndex=0, data_or_wLength=[0xa7,0x00])

#windows driver does all off at the beginning too
all_off(dev)


#do some nice color transitions for 20 seconds
start=time.time()
oldr,oldg,oldb=0,0,0
while time.time()-start<20:
    r,g,b=random_color()
    print "Transitioning to %s,%s,%s"%(r,g,b)
    transition(dev,r,g,b,1,0.001,oldr,oldg,oldb)
    oldr,oldg,oldb=r,g,b

#turn off
transition(dev,0,0,0,1,0.001,oldr,oldg,oldb)
print "good bye"

