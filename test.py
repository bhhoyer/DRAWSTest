#!/usr/bin/env python

import subprocess
from gps import *
import time

revision = 0.0 #unreleased
error = "Error Report:\n"

print "NWDR DRAWS Test Program REV",revision
print

print "Check EEPROM"
subprocess.call(["n7nix/bin/udrcver.sh"])
print

raw_input("Check ADC")
sensors =  subprocess.check_output(["sensors"])
slist =  sensors.splitlines( )
print slist[3]
vstring = slist[3]
vin = float(vstring[24:29])
if 9 < vin < 15:
    print "Vin is OK (9-15V)"
else:
    print "Vin out of range (9-15V)"
    error = error + "Vin out of range (9-15V)\n"
print

raw_input("Check CODEC Control")
cml = subprocess.check_output(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","40 kOhm"])
clist =  cml.splitlines( )
print clist[3]
if clist[3] != "  Item0: '40 kOhm'":
    print "ERROR"
    error = error + "CODEC 40k\n"
else:
    error = error + "CODEC 40k OK\n"
cml = subprocess.check_output(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","10 kOhm"])
clist =  cml.splitlines( )
print clist[3]
if clist[3] != "  Item0: '10 kOhm'":
    print "ERROR"
    error = error + "CODEC 10k\n"
else:
    error = error + "CODEC 10k OK\n"
print

print "Check PTT LEDs"
raw_input("Left PTT ON")
subprocess.call(["gpio","-g","write","12","1"])
raw_input("Right PTT ON")
subprocess.call(["gpio","-g","write","12","0"])
subprocess.call(["gpio","-g","write","23","1"])
print
raw_input("Check GPS, ctl-c to Quit")
subprocess.call(["gpio","-g","write","23","0"])

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 
print 'Latitude\tLongitude\tTime UTC\t\t\tAltitude\tEPV\tEPT\tSpeed\tClimb' # '\t' = TAB to try and output the data in columns.
   
try:
  
    while True:
        report = gpsd.next() #
        if report['class'] == 'TPV':
             
            print  getattr(report,'lat',0.0),"\t",
            print  getattr(report,'lon',0.0),"\t",
            print  getattr(report,'time',''),"\t",
            print  getattr(report,'alt','nan'),"\t\t",
            print  getattr(report,'epv','nan'),"\t",
            print  getattr(report,'ept','nan'),"\t",
            print  getattr(report,'speed','nan'),"\t",
            print  getattr(report,'climb','nan'),"\t"
 
        time.sleep(1.1) 
 
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "Done.\nExiting."
    print

f = raw_input("Press f to Set Up To Flash ")
if f == "f":
	print "FLASH"
    #subprocess.call(["sudo","cp","config.txt.flash","/boot/config.txt"])
    #subprocess.call(["sudo","reboot","now"])
print
print error
# /var/log/udr_install.log

