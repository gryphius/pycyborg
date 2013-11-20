#!/usr/bin/python
"""The emperors new groove"""

from lightshow import LightShow
import sys

show=LightShow()
for _ in range(6):
    show.add_light()

show.soundfile='/home/gryphius/perfectworld.ogg'
#colors
red=(255,0,0)
blue=(0,0,255)
green=(0,255,0)
yellow=(0,255,255)
white=(255,255,255)

#lights
left=[0,1,2]
right=[3,4,5]
all=[0,1,2,3,4,5]

# ---------------------------------------- START
#piano intro
show.set_color(1000,all,white,200)
show.set_color(1200,[0,1,2],(0,0,80),8000)
show.set_color(1200,[3,4,5],(0,80,0),8000)

#trumpet start
ts=9800
show.set_color(ts+0,[3,4,5],red,1500)
show.set_color(ts+700,0,blue,1000)
show.set_color(ts+800,1,blue,1000)
show.set_color(ts+900,2,blue,1000)

show.set_color(11400,all,yellow,1000)
show.set_color(11813,all,green,1000)
show.set_color(12096,all,yellow,1000)
show.set_color(12299,all,green,1000)
show.set_color(12420,all,yellow,1000)
show.set_color(12779,all,green,1000)
show.set_color(13000,all,yellow,1000)

#off hits
show.set_color(15617,all,white,200)
show.set_color(16562,all,white,200)

show.set_color(17060,all,blue,200)
show.set_color(17302,all,red,200)
show.set_color(17391,all,blue,200)

show.set_color(18043,all,white,200)

#---------------- GO ! -------------------------------

show.debug=True
show.debug_all_ts=True

offset=0
end=None
if len(sys.argv)>1: #start in seconds
    offset=int(sys.argv[1])*1000
if len(sys.argv)>2: #play duration in seconds
    end=offset+int(sys.argv[2])*1000
show.play(offset,end)