from distutils.core import setup
import glob
import sys
import os


setup(name = "pycyborg",
    version = "1.0",
    description = "AMBX Cyborg Gaming Lights Library",
    author = "O. Schacher",
    url='https://github.com/gryphius/pycyborg',
    download_url='http://github.com/gryphius/pycyborg/tarball/master',
    author_email = "oli.schacher@gmail.com",
    requires = ['pyusb(>=1.0)'],
    packages = ['pycyborg'],
    long_description = """AMBX Cyborg Gaming Lights Library""" ,
    data_files=[
                ('/etc/udev/rules.d',['doc/80-cyborg.rules']),
                ],
      
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: No Input/Output (Daemon)',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          ],
)


        
        
        