import logging
logger = logging.getLogger(__name__)

import sys
USBLIB_AVAILABLE=False
try:
    import usb.core
    import usb.backend.libusb1 as libusb1
    USBLIB_AVAILABLE=True 
except:
    sys.stderr.write("Could not import usb.core - please make sure pyusb 1.0 is installed into sys.path or symlinked in pycyborg")


import time
import ctypes
import os


# --- device info ---
VENDOR=0x06a3
PRODUCT=0x0dc5
CONFIGURATION=1


# protocol constants

COMMAND={
  'enable':0xa1,
  'color':0xa2,
  'position':0xa4,
  'v_position':0xa5,
  'intensity':0xa6,
  'reset':0xa7,
}

POSITION={
 'CENTER':[0x00,0x01],
 'N':[0x01,0x00],
 'NE':[0x02,0x00],
 'E':[0x04,0x00],
 'SE':[0x08,0x00],
 'S':[0x10,0x00],
 'SW':[0x20,0x00],
 'W':[0x40,0x00],
 'NW':[0x80,0x00],
}

V_POS={
 'any':0x00,
 'low':0x08,
 'middle':0x04,
 'high':0x02
}


def v2k(val,dic):
    for k,v in dic.items():
        if v==val:
            return k


class Cyborg(object):
    def __init__(self,usbdev):
        self.usbdev=usbdev
        self.position=None
        self.vertical_position=None
        self.intensity=None
        
        #keep color values for transitions
        self.r=0
        self.g=0
        self.b=0
        
    def initialize(self,lights_off=True):
        """initialize the device"""
        self.usbdev.set_configuration(CONFIGURATION)
        self._usb_idle_request()
        self._usb_reset_request()
        self._usb_get_report()
        if lights_off:
            self.lights_off()

    def _usb_idle_request(self):
        self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x0a, wValue=0x00, wIndex=0, data_or_wLength=None)

    def _usb_reset_request(self):
        self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a7, wIndex=0, data_or_wLength=[0xa7,0x00])
 
    def _usb_get_report(self):
        """read the cyborg device status like position and intensity"""
        arraydata=self.usbdev.ctrl_transfer(bmRequestType=0xa1, bRequest=0x01, wValue=0x03b0, wIndex=0, data_or_wLength=9)
        data=arraydata.tolist()
        assert (data[0:4]==[0xb0,0x00,0x00,0x01]) or (data[0:4]==[0xb0,0xaa,0x00,0x01]), \
          'unexpected device status info start: %s'%(data[0:4])
        assert data[8]==1,'unexpected last byte value: %s'%data[8]
        position=data[4:6]
        v_pos=data[6]
        self.vertical_position=v2k(v_pos,V_POS)
        self.intensity=data[7]
        self.position=v2k(position,POSITION)
        return(data)
    
    @staticmethod
    def assert_int_255(i):
        """make sure i is an int between 0 and 255"""
        i=int(i)
        if i<0:
            i=0
        if i>255:
            i=255
        return i
     
    def set_rgb_color(self,r=0,g=0,b=0,force=False):
        """Set the light to a specific color immediately"""
        r=self.assert_int_255(r)
        g=self.assert_int_255(g)
        b=self.assert_int_255(b)
        #make this a no-op if we already are showing this color
        if not force and (r==self.r and g==self.g and b==self.b):
            return None
        
        ret=self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a2, wIndex=0, data_or_wLength=[0xa2,0x00,r,g,b,0x00,0x00,0x00,0x00])
        self.r=r
        self.g=g
        self.b=b
        return ret

    def rgb_transition(self,r=0,g=0,b=0,duration=1,force=False):
        """Transition from current color to another. Duration in secs.        
        Timing handled by Cyborg hardware.  Function returns immediately."""
        r=self.assert_int_255(r)
        g=self.assert_int_255(g)
        b=self.assert_int_255(b)
        #make this a no-op if we already are showing this color
        if not force and (r==self.r and g==self.g and b==self.b):
            return None
        
        tms = int(duration*1000)
        assert tms>=0 and tms<=0xffffffff
        t=tms.to_bytes(4,'little')

        logger.info(
            'Transitioning device at %03d:%03d to RGB:%02x%02x%02x over %d ms',
            self.usbdev.bus,self.usbdev.address,r,g,b,tms)
        ret=self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a2, wIndex=0, data_or_wLength=[0xa2,0x00,r,g,b,t[0],t[1],t[2],t[3]])
        self.r=r
        self.g=g
        self.b=b
        return ret
    
    def transition_to(self,r,g,b,duration=1,updatetime=0.001):
        """Transition from current color to another. duration and updatetime in secs"""
        steps=duration/updatetime
        start_r,start_g,start_b=self.r,self.g,self.b
        step_r=(r-start_r)/steps
        step_g=(g-start_g)/steps
        step_b=(b-start_b)/steps
        for step in range(int(steps)):
            time.sleep(updatetime)
            new_r=start_r+(step*step_r)
            new_g=start_g+(step*step_g)
            new_b=start_b+(step*step_b)
            self.set_rgb_color(new_r,new_g,new_b)
            
        self.set_rgb_color(r,g,b)
    
    def lights_off(self):
        self.set_rgb_color(0,0,0)
    
    def set_intensity(self,intensity):
        """sets intensity value (0-100)"""
        intensity=int(intensity)
        assert intensity>=0 and intensity<=100
        self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a6, wIndex=0, data_or_wLength=[0xa6,0x00,intensity])
        self.intensity=intensity
        
    def set_position(self,position):
        """set the device position. allowed values are: CENTER,N,NE,E,SE,S,SW,W,NW"""
        assert position in POSITION
        posbytes=POSITION[position]
        self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a4, wIndex=0, data_or_wLength=[0xa4,0x00,posbytes[0],posbytes[1]])
        self.position=position

    def set_vertical_position(self,verticalposition):
        """set the vertical position. allowed values are: any, low, middle, high"""
        assert verticalposition in V_POS
        posbyte=V_POS[verticalposition]
        self.usbdev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x03a5, wIndex=0, data_or_wLength=[0xa5,0x00,posbyte])
        self.verticalposition=verticalposition

    def __str__(self):
        return "<Cyborg position=%s v_pos=%s intensity=%s%%>"%(self.position,self.vertical_position,self.intensity) 


def is_openelec():
    """Returns True if we are on a openelec system (which means read-only root fs)"""
    if os.path.exists("/etc/openelec-release"):
        return True
    osrelfile="/etc/os-release"
    if os.path.exists(osrelfile) and "openelec" in open(osrelfile,'r').read().lower():
        return True
    return False

def get_all_cyborgs(lights_off=True):
    """Search usb bus for cyborg gaming ligts and return all initialized Cyborg objects"""
    
    if not USBLIB_AVAILABLE:
        return []
    
    retlist=[]
    #patch the dll loader for openelec systems (or we'll get no backend available error)
    if is_openelec():
        def openelec_loader(find_library=None):
            return ctypes.CDLL('libusb-1.0.so')
        
        libusb1._load_library=openelec_loader
    
    devs=usb.core.find(find_all=True,idVendor=VENDOR,idProduct=PRODUCT)
    for dev in devs:
        c=Cyborg(dev)
        try:
            c.initialize(lights_off)
            retlist.append(c)
        except:
            import traceback
            ex=traceback.format_exc()
            sys.stderr.write("Cyborg initialization failed : %s"%ex)

    return retlist


def transition_multiple(cyborgs,targetrgbs,duration=1,updatetime=0.001):
    """transition multiple cyborgs"""
    if len(cyborgs)>len(targetrgbs):
        raise Exception("targetrgbs must be a list of rgb tuples with size>=num cyborgs")
    steps=duration/updatetime
    
    startstep=[]
    
    for i in range(len(cyborgs)):
        cyborg=cyborgs[i]    
        start_r,start_g,start_b=cyborg.r,cyborg.g,cyborg.b
        step_r=(targetrgbs[i][0]-start_r)/steps
        step_g=(targetrgbs[i][1]-start_g)/steps
        step_b=(targetrgbs[i][2]-start_b)/steps
        startstep.append((start_r,start_g,start_b,step_r,step_g,step_b),)
    
    for step in range(int(steps)):
        time.sleep(updatetime)
        for i in range(len(cyborgs)):
            cyborg=cyborgs[i]
            (start_r,start_g,start_b,step_r,step_g,step_b)=startstep[i]
            new_r=start_r+(step*step_r)
            new_g=start_g+(step*step_g)
            new_b=start_b+(step*step_b)
            cyborg.set_rgb_color(new_r,new_g,new_b)
    
    for i in range(len(cyborgs)):
        cyborg=cyborgs[i]
        cyborg.set_rgb_color(targetrgbs[i][0],targetrgbs[i][1],targetrgbs[i][2])
        


if __name__=='__main__':
    cyborgs=get_all_cyborgs()
    print("found %s cyborg gaming lights"%(len(cyborgs)))
    
    for cy in cyborgs:
        print("Cyborg:")
        print(cy)
        cy.set_rgb_color(255,0,0)
        time.sleep(2)
        cy.lights_off()
    
    print("done")
        
    
