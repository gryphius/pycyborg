#!/usr/bin/env python

"""
Boblight interface for pycyborg
"""

import sys
import os
from pycyborg import get_all_cyborgs

try:
  raw_input
except NameError:
  pass
else:
  def input(msg=''):
    return(raw_input(msg))

	
cyborgs=get_all_cyborgs()

positions={
      'CENTER':{'hscan':'33.3 66.6','vscan':'33.3 66.6'},
      'N':{'hscan':'33.3 66.6','vscan':'0 33.3'},
      'NE':{'hscan':'66.6 100','vscan':'0 33.3'},          
      'E':{'hscan':'66.6 100','vscan':'33.3 66.6'},
      'SE':{'hscan':'66.6 100','vscan':'66.6 100'},
      'S':{'hscan':'33.3 66.6','vscan':'66.6 100'},
      'SW':{'hscan':'0 33.3','vscan':'66.6 100'},
      'W':{'hscan':'0 33.3','vscan':'33.3 66.6'},
      'NW':{'hscan':'0 33.3','vscan':'0 33.3'},
    }

def bobloop():
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
    

def ask_position(current_position=None):
    while True:
        if current_position!=None:
            new_pos=input("New position [%s]: "%current_position)
        else:
            new_pos=input("Position (one of: %s: "%",".join(list(positions.keys())))
        new_pos=new_pos.upper()
        if new_pos=='' and current_position!=None:
            return current_position
        if new_pos in list(positions.keys()):
            return new_pos
        print("please enter one of: %s"%",".join(list(positions.keys())))
    
    

def config_wizard():
    #get number of cyborgs
    num_cyborgs=len(cyborgs)
    message="I have detected %s cyborgs. Press Enter to create a config for these or enter the number of cyborgs you want to configure: "%num_cyborgs
    if num_cyborgs==0:
        message="No cyborgs detected automatically. How many cyborgs do you have?"
        
    use_detected_cyborgs=False
    num=None
    
    while True:
        inp=input(message)
        if inp.strip()=='':
            num=num_cyborgs
            use_detected_cyborgs=True
            break
        
        try:
            n=int(inp)
            num=n
            break
        except:
            print("uhm...apparently I wasn't clear enough...please enter a number or press enter")
    
    if num==0:
        print("Ok, no cyborgs it is.. that config was fairly easy to create. cya.")
        sys.exit(0)
    
    #create empty config
    config=[None for i in range(num+1)]
            
    #prefill known values
    
    
    if use_detected_cyborgs:
        for i in range(num):
            current_cyborg=cyborgs[i]
            config[i]=current_cyborg.position
        
    #go over unknown cyborgs
    for i in range(num):
        print("Checking: Cyborg No. %s"%(i+1))
        if config[i]!=None:
            print("Current position is: %s"%config[i])
            continue
        print("No position found so far.")
        if use_detected_cyborgs:
            cyborgs[i].set_rgb_color(255,255,255)
        config[i]=ask_position()
        if use_detected_cyborgs:
            cyborgs[i].lights_off()
    
    
    #menu
    inp=None
    while inp!='done':
        print("Ok, here's the current setup:")
        print("")
        
        
        for i in range(num):
            print("[%s] : %s"%(i+1,config[i]))
            
        print("")
        print("enter number to change position, or 'done' to create the config")
        inp=input().lower()
        
        try:
            ind=int(inp)-1
            
            if use_detected_cyborgs:
                cyborgs[ind].set_rgb_color(255,255,255)
            config[ind]=ask_position(config[ind])
            if use_detected_cyborgs:
                cyborgs[ind].lights_off()
                cyborgs[ind].set_position(config[ind])
            
            
        except:
            continue
    
        
    #generate the config
    mypath=os.path.abspath(__file__)
    channels=num*3
    header="""[global]
interface 127.0.0.1
port 19333

[device]
name cyborg_ambx
output %s
channels %s
type popen
interval 500000

[color]
name red
rgb FF0000

[color]
name green
rgb 00FF00

[color]
name blue
rgb 0000FF
    """%(mypath,channels)
    
    output=header
    
    channel_counter=0

    for i in range(num):
        output+="\n[light]\n"
        output+="name cyborg-%s-%s\n"%(i,config[i])
        channel_counter+=1
        output +="color red cyborg_ambx %s\n"%channel_counter
        channel_counter+=1
        output +="color green cyborg_ambx %s\n"%channel_counter
        channel_counter+=1
        output +="color blue cyborg_ambx %s\n"%channel_counter
        for k,v in positions[config[i]].items():
            output+="%s %s\n"%(k,v)
    
    if use_detected_cyborgs:  
        for cy in cyborgs:
                cy.lights_off()
    return output

if __name__=='__main__':
    if '--makeconfig' in sys.argv:
        content=config_wizard()
        file_name=input("Enter a filename where I should store the newly generated config or press enter to display only:\n")
        file_name=file_name.strip()
        if file_name!='':
            fh=open(file_name,'w')
            fh.write(content)
            fh.close()
            print("%s written successfully."%(file_name))
            sys.exit(0)
        else:
            print(content)
            sys.exit(0)
        
    try:
        bobloop()
    except KeyboardInterrupt:
        for cy in cyborgs:
            cy.lights_off()

