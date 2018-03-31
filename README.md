# cellar_ventilation
This code is written in Python 3 (used the Anaconda Framework) and is supposed to run on a raspberrypi
There is additional Hardware neccessary. 
  - 2x DHT22 humidity sensors 
  - a relais for activating the motor that opens/closes the window
  - the motor on the window
keller.py 
is supposed to run every 10 min. It's the main file for making the decision to ventilate or not; i used a cronjob to do that.
a logfile (luftfeuchtelog.txt) will be created and every measurement will be appended to it in a new line 

lflog.py 
is used to create a chart from the data and sends it via mail

mail.py as well as plotten.py 
are used for sending the mail and creating a chart

temp_uw.py and templog.py do pretty much the same as keller.py and lflog.py without the second sensor and a missing actor.

