#!/usr/bin/env python

import subprocess
from gps import *
import time

revision = 0.0 #unreleased
error = "Error Report:\n"

print "NWDR DRAWS Test Program REV",revision
time.sleep(1)
print

print "Check EEPROM "
subprocess.call(["n7nix/bin/udrcver.sh"])
print

raw_input("Check ADC ")
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

raw_input("Check CODEC Control ")
cerr = 0
cml = subprocess.check_output(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","40 kOhm"])
clist =  cml.splitlines( )
if clist[3] != "  Item0: '40 kOhm'":
    cerr = cerr + 1
cml = subprocess.check_output(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","10 kOhm"])
clist =  cml.splitlines( )
if clist[3] != "  Item0: '10 kOhm'":
    cerr = cerr + 1
if cerr != 0:
    print "CODEC Control Fail"
    error = error + "CODEC Control Fail\n"
else:
    print "CODEC Control OK"
print

print "Check PTT LEDs"
raw_input("Left PTT ON ")
subprocess.call(["gpio","-g","write","12","1"])
raw_input("Right PTT ON ")
subprocess.call(["gpio","-g","write","12","0"])
subprocess.call(["gpio","-g","write","23","1"])
print

raw_input("Check GPS for time advancing and serial sentences\nctl-c to Quit ")
subprocess.call(["gpio","-g","write","23","0"])

try:
    subprocess.call(["gpsmon"])    
except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    time.sleep(1)
    print "Exiting\n"
    
print error
