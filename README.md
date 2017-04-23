# pycyborg

Python library for the mad catz cyborg ambx gaming lights 
(http://www.ambx.com/product/cyborg-gaming-lights)

## Status
 - protocol reverse engineering: done
 - simple demo without library: done
 - library: done
 - boblight interface: done
 - installer: done
 - tested platforms: Linux(Arch,Ubuntu,OpenElec,Raspbian) , Mac OS X, Win10

Requires : 
 - libusb 1.0 ( http://www.libusb.org/ ) or libusb-win32 (http://zadig.akeo.ie/)
 - pyusb  ( https://github.com/walac/pyusb/ )

## scripts

* ```identify.py``` : activate all cyborg gaming lights and print out some information
* ```setcolor.py``` : control the gaming lights from the shell (from bash scripts etc) 
* ```boblight.py``` : boblight interface
* ```lightpack-prismatik.py``` : [lightpack](http://lightpack.tv/index.php) client
* a few demo scripts are available in the ```demo``` folder 

## getting started

* install libusb-1.0 (or libusb-win32 via zadig)
* install pyusb 1.0 ( use your distro's package or directly from  github: https://github.com/walac/pyusb/ )
* get the source

either as package:

    wget http://github.com/gryphius/pycyborg/tarball/master -O pycyborg.tar.gz
    tar -xvzf pycyborg.tar.gz
    cd gryphius-pycyborg*
    
or clone git repo

    git clone git://github.com/gryphius/pycyborg.git
    cd pycyborg


* install

install the package and reload udev rules

    python setup.py install
    sudo udevadm trigger

* test

this should flash your gaming lights and print out some info. 
if you skipped step 2 you must run this as root, eg. sudo python identify.py or you will get ```USBError: [Errno 13] Access denied``` (insufficient permissions)

    python identify.py
 

console output should be similar to this:

    found and initialized 2 cyborg ambx gaming lights
    	
    Cyborg 1: 
    <Cyborg position=NW v_pos=low intensity=50%>
    
    Cyborg 2: 
    <Cyborg position=S v_pos=low intensity=50%>


## boblight

To control the cyborg lights from boblight (http://code.google.com/p/boblight/), use a config file like below
(change the path in 'output' to where you checked out pycyborg)


	[global]
	interface 127.0.0.1
	port 19333
	
	[device]
	name cyborg_ambx
	output /home/gryphius/gitspace/pycyborg/boblight.py
	channels 6
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
	
	[light]
	name cyborg-left
	color red cyborg_ambx 1
	color green cyborg_ambx 2
	color blue cyborg_ambx 3
	hscan 0 49.9
	vscan 0 100
	
	[light]
	name cyborg-right
	color red cyborg_ambx 4
	color green cyborg_ambx 5
	color blue cyborg_ambx 6
	hscan 50 100
	vscan 0 100


there is also a simple wizard that can automatically generate a config file. this is especially useful if you have more than two lights: 


    python boblight.py --makeconfig
 
