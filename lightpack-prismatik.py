#!/usr/bin/python
import socket
import time
import traceback
from pycyborg import get_all_cyborgs,transition_multiple
import sys

class PrismatikClient(object):
    def __init__(self,host='localhost',port=3636,apikey=None):
        self.host=host
        self.port=port
        self.apikey=apikey
        self.clientsocket=None
        self.socketfile=None
        self.update_interval=0.2 
        self.cyborgs=get_all_cyborgs()
        
    def _reconnect(self):
        self.clientsocket=None
        self.socketfile=None
        reconnect_interval=3
        s=None
        while s==None:
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect((self.host,self.port),)
            except Exception,e:
                s=None
                print "Connection failed, retrying in %s seconds. Reason: %s"%(reconnect_interval,str(e))
                time.sleep(reconnect_interval)
        
        self.clientsocket=s
        self.socketfile=self.clientsocket.makefile('r')
        banner=self.socketfile.readline()
        print "Connected/%s"%banner
        if self.apikey:
            self.authenticate()
    
    def authenticate(self):
        res=self.command('apikey:%s'%self.apikey)
        assert res=='ok','authentication failed: %s'%res

    def command(self,command):
        self.clientsocket.sendall('%s\r\n'%command)
        return self.socketfile.readline().strip()

    def update_light_state(self):
        colorline=self.command('getcolors')
        keyword='colors:'
        if not colorline.startswith(keyword):
            raise Exception('unexpected reply: %s'%colorline)
        
        all_colorinfo=colorline[len(keyword):]
        colorinfos=all_colorinfo.split(';')
        
        targets=[]
        for colorinfo in colorinfos:
            colorinfo=colorinfo.strip()
            if colorinfo=='':
                continue
            lightindex,rgb=colorinfo.split('-')
            r,g,b=map(int,rgb.split(','))
            targets.append((r,g,b),)
        transition_multiple(self.cyborgs,targets,duration=0.3)
        

    def run(self):
        while True:
            if self.clientsocket==None:
                self._reconnect()
            try:
                self.update_light_state()
                time.sleep(self.update_interval)
            except KeyboardInterrupt:
                for c in self.cyborgs:
                    c.lights_off()
                return
            except Exception,e:
                print traceback.format_exc()
                print "Connection broken. reconnecting. (%s)"%(str(e))
                self._reconnect()
            
if __name__=='__main__':
    if len(sys.argv)<2:
        print "args: <apikey> [<host>]"
    apikey=sys.argv[1]
    if len(sys.argv)<3:
        host='localhost'
    else:
        host=sys.argv[2]
        
    client=PrismatikClient(host,apikey=apikey)
    client.run()
