#!/usr/bin/python
"""The emperors new groove"""

from lightshow import LightShow
from colors import *
import sys
import random
import os

show=LightShow()
show.audiodelay_offset=0

for _ in range(6):
    show.add_light()

show.soundfile=os.path.expanduser('~/perfectworld.ogg')

# --- ALIAS SETUP --- #

#lights
L1=0
L2=1
L3=2
L4=3
L5=4
L6=5

#custom colors
green=android_green

def choruslight(light,pos):
    switchtime=1000.0
    offset_per_light=switchtime*2/6
    
    #strophe 1
    color1=spring_green
    color2=light_sky_blue
    
    #strophe2
    if pos>35839:
        color1=cyan
        color2=hot_magenta
    
    #bridge
    if pos>54127:
        color1=green_crayola
        color2=han_blue
    
    #pitch change1
    if pos>86316:
        color1=electric_violet
        color2=deep_sky_blue
        
    #pitch change2
    if pos>90700:
        color1=violet
        color2=cg_red
    
    diff_r=color2[0]-color1[0]
    diff_g=color2[1]-color1[1]
    diff_b=color2[2]-color1[2]
    step_r=diff_r/switchtime
    step_g=diff_g/switchtime
    step_b=diff_b/switchtime
    abspos=(pos+light*offset_per_light)%(switchtime*2)
    if abspos>switchtime:
        abspos=switchtime*2-abspos
    
    
    new_r=color1[0]+abspos*step_r
    new_g=color1[1]+abspos*step_g
    new_b=color1[2]+abspos*step_b
        
    return int(new_r),int(new_g),int(new_b)

#lights
left=[L1,L2,L3]
right=[L4,L5,L6]
all=[L1,L2,L3,L4,L5,L6]

# ---------------------------------------- START
print "Intro..."
#piano intro
show.set_color(1000,all,white,200)
start=1200
dur=2000
for i in range(4):
    st=int(start+i*dur/2)
    show.transition(st,[L1,L3,L5],aquamarine,bittersweet,dur)
    show.transition(st,[L2,L4,L6],bittersweet,aquamarine,dur)
    st=st+int(dur/2)
    show.transition(st,[L1,L3,L5],bittersweet,aquamarine,dur)
    show.transition(st,[L2,L4,L6],aquamarine,bittersweet,dur)

#trumpet start
show.set_color(8600,all,white,2000) #00:08 
show.set_color(8808,L5,dark_orchid,1000) #00:08 
show.set_color(8859,L4,dark_orchid,1000) #00:08 
show.set_color(8993,L3,dark_orchid,1000) #00:08 
show.set_color(9215,L2,dark_orchid,1000) #00:09 

#blackout before hit
show.set_color(9607,all,black,1000) #00:09 


show.set_color(9838,all,white,1500) #00:09
show.set_color(10380,L2,neon_fuchsia,500) #00:10 
show.set_color(10480,L4,neon_fuchsia,500) #00:10 
show.set_color(10600,L6,neon_fuchsia,300) #00:10 

duration=1000
show.set_color(11417,all,bright_pink,duration) #00:11 
show.set_color(11736,all,bright_turquoise,duration) #00:11 
show.set_color(11974,all,bright_pink,duration) #00:11 
show.set_color(12222,all,bright_turquoise,duration) #00:12 
show.set_color(12300,all,bright_pink,duration) #00:12 
show.set_color(12664,all,bright_turquoise,duration) #00:12 
show.set_color(12926,all,bright_pink,duration) #00:12 


#random colors
for pos in range(13770,15369): #00:13-00:15
    randomcolor=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    show.set_color(pos,all,randomcolor,1)
    

#off hits
show.set_color(15617,all,chrome_yellow,200)
show.set_color(16462,all,daffodil,200)

#triole
show.set_color(17100,[L1,L2],ultra_pink,600)
show.set_color(17202,[L3,L4],tiffany_blue,500)
show.set_color(17291,[L5,L6],veronica,300)

show.set_color(17995,all,scarlet,200)


print "chorus 1..."
#00:19 strophe1
for i in range(120000):
    pos=19000+i
    for light in all:
        color=choruslight(light, pos)
        show.set_color(pos,light,color,1)

#hits am ende
show.set_color(32573,all,lemon_lime,200) #00:32 
show.set_color(33838,all,cadmium_orange,200) #00:33 
show.set_color(34249,all,white,800) #00:34 
show.set_color(34349,L1,red,100) #00:34
show.set_color(34399,L2,red,100) #00:34
show.set_color(34449,L3,red,100) #00:34
show.set_color(34499,L4,red,100) #00:34
show.set_color(34549,L5,red,100) #00:34
show.set_color(34599,L6,red,100) #00:34


show.set_color(34700,all,black,2100) #00:34 

print "chorus 2..."
## 00:38 strophe2 ##


#triplehit
show.set_color(52523,[L1,L6],school_bus_yellow,600) #00:52 
show.set_color(52670,[L2,L5],screamin_green,400) #00:52 
show.set_color(52794,[L3,L4],shocking_pink,200) #00:52

show.set_color(53833,all,wild_strawberry,1000) #00:53 
show.set_color(54032,[L2,L3],tractor_red,800) #00:54 
show.set_color(54380,[L3,L4],yellow,600) #00:54 
show.set_color(54594,[L4,L5],vivid_violet,400) #00:54 

print "bridge..."
#00:55 bridge

show.set_color(59138,all,white,200) #00:59 



show.set_color(61550,[L1,L2],red,100) #01:01 
show.set_color(61716,[L3,L4],red,100) #01:01 
show.set_color(61803,[L5,L6],red,100) #01:01 

show.set_color(62064,[L5,L6],harlequin,100) #01:02 
show.set_color(62196,[L3,L4],harlequin,100) #01:02 
show.set_color(62335,[L1,L2],harlequin,100) #01:02 

show.set_color(62476,all,banana_yellow,100) #01:02 
show.set_color(62831,all,red,100) #01:02 
show.set_color(63065,all,banana_yellow,100) #01:03 

#prepare break
show.set_color(68151,[L2,L3,L4,L5],bright_green,1000) #01:08 
show.set_color(69310,[L2,L3,L4,L5],aureolin,1000) #01:09 

#break
show.set_color(70706,all,magenta,200) #01:10 
show.set_color(71702,all,mango_tango,200) #01:11 

print "refrain..."
#01:12 refrain (whats his name...)
show.set_color(72727,all,red,1000) #01:12 

show.set_color(73200,[L1,L2],black,1000) #01:12 
show.set_color(73350,[L3,L4],black,1200) #01:12 
show.set_color(73500,[L5,L6],black,1300) #01:12 


show.set_color(81176,[L1,L6],yellow,1000) #01:21                                                                                                                                                               
show.set_color(81266,[L2,L5],yellow,1000) #01:21                                                                                                                                                               
show.set_color(81475,[L3,L4],yellow,1000) #01:21                                                                                                                                                               
show.set_color(81567,all,yellow,1000) #01:21   


print "pitch shift..."
#01:31 tonartwechsel

#sax
show.set_color(97439,all,black,2000) #01:37 
color=bright_pink

#right
start=97500

offset=int(350.0/6.0)
show.set_color(start+0*offset,L1,color,100) #01:37 
show.set_color(start+1*offset,L2,color,100) #01:37 
show.set_color(start+2*offset,L3,color,100) #01:37
show.set_color(start+3*offset,L4,color,100) #01:37
show.set_color(start+4*offset,L5,color,100) #01:37
show.set_color(start+5*offset,L6,color,100) #01:37

#left
color=dark_orange
show.set_color(start+6*offset,L6,color,100) #01:37 
show.set_color(start+7*offset,L5,color,100) #01:37 
show.set_color(start+8*offset,L4,color,100) #01:37
show.set_color(start+9*offset,L3,color,100) #01:37
show.set_color(start+10*offset,L2,color,100) #01:37
show.set_color(start+11*offset,L1,color,100) #01:37


#hits after sax
show.set_color(98385,all,medium_aquamarine,200) #01:38 
show.set_color(98700,L4,color,100) #01:37
show.set_color(98800,L3,color,100) #01:37
show.set_color(98946,all,carmine_red,200) #01:38 



#what's his name -hit hit
show.set_color(104156,all,deep_sky_blue,2000) #01:44 
show.set_color(105260,all,daffodil,2000) #01:45 
show.set_color(106715,all,white,200) #01:46 
show.set_color(107627,all,white,200) #01:47 
show.set_color(107800,all,black,500) #01:47
show.transition(108671,all,red,bittersweet_shimmer,500) #01:48

#end
show.set_color(133000,all,black,10000) #02:13 
show.set_color(133274,all,magenta,200) #02:13 
show.set_color(134444,all,harlequin,200) #02:14 
show.set_color(134939,all,indigo,200) #02:14 
show.set_color(135520,[L1,L3,L5],red,1000) #02:15 
show.set_color(135520,[L2,L4,L6],white,1000) #02:15

#---------------- GO ! -------------------------------
print "pygame startup..."

offset=0
end=None
if len(sys.argv)>1: #start in seconds
    offset=int(sys.argv[1])*1000
if len(sys.argv)>2: #play duration in seconds
    end=offset+int(sys.argv[2])*1000
show.play(offset,end)
