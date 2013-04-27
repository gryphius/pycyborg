pycyborg
========

Python library for the cyborg ambx gaming lights 
(http://www.cyborggaming.com/de/prod/ambx.htm)


Status:
 - protocol reverse engineering: done
 - simple demo without library: done
 - library: done
 - boblight interface: done
 - installer: todo
 - tested plattforms: Linux

Requires : 
 - pyusb 1.0 ( https://github.com/walac/pyusb/ )


Run "colortransitiondemo.py" for a quick test of a single cyborg gaming light (doesn't use the full library - this was the first test script)

Run "identify.py" to activate all cyborg gaming lights and print out some information (position, intensity)


A boblight (http://code.google.com/p/boblight/) is available. Sample configuration in doc/boblight.conf, adapt path to boblight.py
