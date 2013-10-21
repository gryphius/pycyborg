raspberry pi boblight server
============================

instead of fiddling with drivers and long cables from my media center PC I wanted to have a small "satellite" system to handle the ambilight stuff.
A raspberry pi is perfect for that purpose

Preparation
-----------

* install raspbian on your raspberry pi


Install software
----------------

* compile and install boblight (detailed instrutions: https://code.google.com/p/boblight/wiki/LPD8806_on_Raspberry_Pi#Installation ) here's the sort version:

	sudo apt-get install subversion
	cd ~
	svn checkout http://boblight.googlecode.com/svn/trunk/ boblight-read-only
	cd boblight-read-only/
	./configure --without-portaudio --without-x11 --without-libusb
	make
	sudo make install
	

* install libusb, pyusb and pycyborg

	sudo apt-get install libusb-1.0
	
	cd ~
	git clone https://github.com/walac/pyusb.git
	cd pyusb
	sudo python setup.py install
	
	cd ~
	git clone https://github.com/gryphius/pycyborg.git
	cd pycyborg
	sudo python setup.py install
	sudo udevadm trigger
	

Configuration
-------------
	
* create boblight config

	cd ~/pycyborg
	./boblight.py --makeconfig


* configure the locations of your lights
* when asked for a filename, enter `boblight-new.conf`
* edit the generated boblight-new.conf and replace 127.0.0.1 with 0.0.0.0 so remote systems can connect
* copy the new file to the correct location

	sudo cp boblight-new.conf /etc/boblight.conf
	
* test your configuration by starting `boblightd` manually and configure for example the xbmc boblight addon to connect to your raspi

* make boblight start automatically on boot: edit `/etc/rc.local` and add (before the `exit 0` line)

	/usr/local/bin/boblightd -f

    
