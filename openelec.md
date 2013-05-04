pycyborg installation instructions for openelec
===============================================

Openelec's root filesystem is read-only and there are tools like git missing, therefore the installation steps are a little bit different.

you need: a 2nd computer with network access to the openelec box. this box can be running windows or linux. it needs to have ssh and SMB access to the openelec box.
we'll call that computer **(INSTALLBOX)** from now on. All commands on openelec should be run as root (ssh root@<your openelec ip> - default password is openelec).
We'll call this **(OPENELEC-SSH)**. Stuff that needs to be done in xbmc gui will be tagged **(OPENELEC-XBMC)**


**(OPENELEC-XBMC)**

* enable the ssh service in openelec settings
* install boblightd and boblight xbmc addon
* restart openelec box


**(INSTALLBOX)**

 * download pyusb as zipfile: https://github.com/walac/pyusb/archive/master.zip
 * extract master.zip
 * delete master.zip
 * download pycyborg as zipfile: https://github.com/gryphius/pycyborg/archive/master.zip
 * extract master.zip
 * delete master.zip
 * you should now have two folders "pyusb-master" and "pycyborg-master"
 * copy both folders via smb to the openelec box into "Userdata"
 * in Userdata/addon_data/service.multimedia.boblightd, rename boblight.X11.sample to boblight.X11
 * in the same directory, create a new file 'boblight.conf' with the following content:
 

	[global]
	interface 127.0.0.1
	port 19333
	
	[device]
	name cyborg_ambx
	output "/storage/.xbmc/userdata/pycyborg-master/boblight.py"
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


**(OPENELEC-SSH)**

since we can not install pyusb into a systemfolder where pycyborg can find it, we need to symlink it directly:

	cd ~/.xbmc/userdata/pycyborg-master/
	ln -s ../pyusb-master/usb
	
now it's time to test if the gaming lights are working:

	cd ~/.xbmc/userdata/pycyborg-master/
	./identify.py
	
if you see the lights flashing, another reboot should do the trick and enable boblight

