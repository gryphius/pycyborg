import traceback
import time
import pygame
import sys
import os
sys.path.insert(0,'../../')

from pycyborg import get_all_cyborgs

class PGdisplay(object) :
    screen = None;

    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib','x11']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                #print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        #print "Framebuffer size: %d x %d" % (size[0], size[1])
        if driver=='x11':
            size = (1024,768)
            self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        else:
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def update(self,text,lightstates):
        background = pygame.Surface(self.screen.get_size())
        background = background.convert()
        
        #white background
        background.fill((255,255,255))
        
        #position
        font = pygame.font.Font(None, 30)
        lineoffset=0
        for line in text.split("\n"):
            rtext = font.render(line, 1, (10, 10, 10))
            trec=rtext.get_rect()
            textpos = trec
            textpos.y = 20+lineoffset
            lineoffset+=25
            background.blit(rtext, textpos)
        
        
        #lights
        hoffset=165
        hstart=100
        vpos=400
        radius=80
        texthoffset=30
        textvoffset=20
        for i in range(len(lightstates)):
            state=lightstates[i]
            hpos=hstart + i*hoffset
            tpl=state.rgbtuple()
            rtext = font.render(str(tpl), 1, (10, 10, 10))
            trec=rtext.get_rect()
            textpos = trec
            textpos.x=hpos-radius+texthoffset
            textpos.y=vpos+radius+textvoffset
            background.blit(rtext,textpos)
            border=0
            #fill
            try:
                pygame.draw.circle(background,tpl,(hpos,vpos),radius,border)
            except TypeError:
                print "got onvalid color: %s"%(str(tpl))
                
            #border
            pygame.draw.circle(background,(0,0,0),(hpos,vpos),radius,2)

        # Blit everything to the screen
        self.screen.blit(background, (0, 0))
        pygame.display.flip()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type== pygame.KEYDOWN:
                return event.key
            



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
        
        #use this to offset the audiodelay on slow devices
        self.audiodelay_offset=0
        
        
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

    def transition(self,ts,lights,startcolor,endcolor,duration):
        """Transition from current color to another. duration and updatetime in secs"""
        steps=duration
        r,g,b=endcolor
        start_r,start_g,start_b=startcolor
        step_r=(r-start_r)/float(steps)
        step_g=(g-start_g)/float(steps)
        step_b=(b-start_b)/float(steps)
        for step in range(int(steps)):
            new_r=int(start_r+(step*step_r))
            new_g=int(start_g+(step*step_g))
            new_b=int(start_b+(step*step_b))
            if new_r<0 or new_g<0 or new_b<0:
                print new_r,new_g,new_b
            for light in lights:
                self.states[light][ts+step]=LightState(new_r,new_g,new_b)

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
        
        #load track with sound to get total length
        soundfile=self.soundfile
        totalpos=int(pygame.mixer.Sound(soundfile).get_length()*1000)
        totalpos_str=self._ms_to_minsec(totalpos)
        pygame.mixer.music.load(soundfile)
        secoffset=int(offset/1000.0)
        pygame.mixer.music.play(0,secoffset)
        ticktime=0.001
        lightsoff=LightState(0,0,0)
                

        display=PGdisplay()
        
        
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
                
                states=[]
                for light in range(self.get_num_lights()):
                    state=self.get_state(ts-self.audiodelay_offset, light)
                    if state==None:
                        state=lightsoff
                    states.append(state)
                    
                    
                    if light<num_cyborgs:
                        cyborgs[light].set_rgb_color(state.r,state.g,state.b)
                
                message="Track: %s msec=%s time=%s\n"%(soundfile,totalpos,totalpos_str)     
                message+="Position: %s\n"%(ts)
                message+="Time: %s\n"%(self._ms_to_minsec(ts))
                key=display.update(message, states)
                if key==pygame.K_c:
                    savedpositions.append(ts)
                time.sleep(ticktime)
        except KeyboardInterrupt:
            pass
        except Exception:
            trb=traceback.format_exc()
        for cyborg in cyborgs:
            cyborg.lights_off()
        
        if trb!=None:
            print trb
        
        if len(savedpositions)>0:
            print "Saved positions: %s"%savedpositions
            for s in savedpositions:
                print """show.set_color(%s,lightlist,color,duration) #%s """%(s,self._ms_to_minsec(s))
    
if __name__=='__main__':
    pass
    
                
    