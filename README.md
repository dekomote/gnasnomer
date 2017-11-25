# gnasnomer
Software for pollution measuring device running on raspberry pi

## What is this repository for? ###

* Gnasnomer
* 0.1.0

### How do I get set up? ###

pip install -e git+https://github.com/dekomote/gnasnomer.git\#egg\=gnasnomer

or 

clone and do setup.py install.

### How do I run it? ###

Install deps listed in requirements.txt if not already installed then

Check usage: magnet2torrent -h

Runs on GNU/Linux and you need the serial pollution sensor (SDS family)
Optionally, if you stick a GPS device and run the gpsd daemon, it will also gather
and post GPS coordinates as to where the reading was done.
