import traceback
import time
import pygame
import curses
import sys
sys.path.insert(0,'../../')

from pycyborg import get_all_cyborgs

class LightState(object):
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b

    def rgbtuple(self):
        return (self.r,self.g,self.b)
    
    def __str__(self):
        return str(self.rgbtuple())
    
    def __eq__(self,other):
        if other==None:
            return False
        return (self.r==other.r and self.g==other.g and self.b==other.b)
    
    def __ne__(self,other):
        return not self.__eq__(other)
        
class LightShow(object):
    def __init__(self):
        self.states=[]
        self.debug=False
        self.debug_all_ts=False
        self.debug_lightsoff=False
        
        self.soundfile=None
    
    def get_num_lights(self):
        return len(self.states)
        
    def add_light(self):
        self.states.append({})
        
    def set_color(self,ts,lights,color,duration):
        if type(lights)!=list:
            lights=[lights,]
            
        for light in lights:
            for d in range(duration):
                self.states[light][ts+d]=LightState(color[0],color[1],color[2])
    
    def get_state(self,ts,light):
        try:
            res=self.states[light][ts]
        except:
            res=None
        return res
    
    def _ms_to_minsec(self,ms):
        totalsec=ms/1000
        mins=totalsec/60
        remainingsec=totalsec-mins*60
        return "%02d:%02d"%(mins,remainingsec)
    
    def play(self,offset=0,end=None):
        trb=None
        pygame.mixer.init()
        pygame.mixer.music.load(self.soundfile)
        secoffset=int(offset/1000.0)
        pygame.mixer.music.play(0,secoffset)
        ticktime=0.001
        lightsoff=LightState(0,0,0)
                
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.border(0)
        stdscr.keypad(1)
        stdscr.nodelay(1)
        
        maxposcount=25
        poswin=curses.newwin(maxposcount+1,20,3,90)
        poswin.border(0)
        
        
        savedpositions=[]
        
        cyborgs=get_all_cyborgs()
        num_cyborgs=len(cyborgs)
        cont=True
        try:
            while cont:
                if not pygame.mixer.music.get_busy():
                    break
                
                ts=pygame.mixer.music.get_pos()+offset
                
                if end!=None and ts>=end:
                    break
                
                stdscr.addstr(1,2, "Position: %s  %s"%(ts,self._ms_to_minsec(ts)))
                stdscr.addstr(2,2, "Cyborgs detected: %s Used: %s"%(num_cyborgs,self.get_num_lights()))
                for light in range(self.get_num_lights()):
                    state=self.get_state(ts, light)
                    strstate=str(state)
                    if state==None:
                        state=lightsoff
                        strstate=""                    
                    stdscr.addstr(10+light,2, "Light %s: %s                    "%(light,strstate))
                    
                    if light<num_cyborgs:
                        cyborgs[light].set_rgb_color(state.r,state.g,state.b)
                        
                        
                    
                stdscr.refresh()
                
                #keypress
                c=stdscr.getch()
                    
                if c==ord('c'):
                    savedpositions.append(ts)
                
                poswin.addstr(1,1,"'c':record pos")
                disp=savedpositions[-maxposcount:]
                for i in range(len(disp)):
                    curpos=disp[i]
                    poswin.addstr(2+i,1,str(curpos))
                poswin.refresh()
                
                time.sleep(ticktime)
        except KeyboardInterrupt:
            pass
        except Exception:
            trb=traceback.format_exc()
        for cyborg in cyborgs:
            cyborg.lights_off()
        
        curses.nocbreak(); stdscr.keypad(0); curses.echo()
        curses.endwin()
        if trb==None:
            print "clean shutdown"
        else:
            print trb
        
        if len(savedpositions)>0:
            print "Saved positions: %s"%savedpositions
    
if __name__=='__main__':
    show=LightShow()
    print show._ms_to_minsec(85000)
    for _ in range(2):
        show.add_light()
    
    show.set_color(0, 0, (255,0,0), 100)
    show.set_color(101, [0,1],(0,0,255), 100)
    
    assert show.get_state(50, 0).rgbtuple()==(255,0,0)
    
                
    