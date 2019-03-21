#!/usr/bin/env python

import subprocess
import time
import sys

revision = 0.1 #unreleased
print "NWDR DRAWS Test Program REV",revision
print

error = "Error Report:\n"

print "Check EEPROM"
hat = subprocess.check_output(["ls","/proc/device-tree/"])
if hat.find("hat\n") != -1:
    name = subprocess.check_output(["cat","/proc/device-tree/hat/name"])
    product = subprocess.check_output(["cat","/proc/device-tree/hat/product"])
    product_id = subprocess.check_output(["cat","/proc/device-tree/hat/product_id"])
    product_ver = subprocess.check_output(["cat","/proc/device-tree/hat/product_ver"])
    uuid = subprocess.check_output(["cat","/proc/device-tree/hat/uuid"])
    vendor = subprocess.check_output(["cat","/proc/device-tree/hat/vendor"])
    print vendor
    print product
    assy_rev = product_ver[2:4]
    fab_rev = product_ver[5:7]
    print "ASSY Rev",assy_rev,"FAB Rev",fab_rev
else:
    print "HAT not Found!"
    sys.exit()
print  
image = subprocess.check_output(["head","-n 1","/var/log/udr_install.log"])
print image[25:]
#print image[:24]

#print "Check Drivers Loaded"
drivers = subprocess.check_output(["lsmod"])
#print drivers
if drivers.find("ads1015") == -1:
    print "ads1015 not loaded"
if drivers.find("sc16is7xx") == -1:
    print "sc16is7xx not loaded"
if drivers.find("tlv320aic32") == -1:
    print "tlv320aic32x4 not loaded"
if drivers.find("tlv320aic32x4_i2c") == -1:
    print "tlv320aic32x4_i2c not loaded"
else:
    print "Drivers Loaded"
print
    
raw_input("Check ADC ")
sensors =  subprocess.check_output(["sensors"])
slist =  sensors.splitlines()
print slist[3]
vstring = slist[3]
vin = float(vstring[24:29])
if 9 < vin < 15:
    print "Vin is OK (9-15V)"
else:
    print "Vin out of range (9-15V)"
    error = error + "Vin out of range (9-15V)\n"
print

raw_input("Check CODEC ")
'''
cerr = 0
hpg = subprocess.check_output(["amixer","-c","0","sset","HP Driver Gain","10"])
clist =  hpg.splitlines()
if clist[5] != "  Front Left: 10 [29%] [4.00dB]":
    cerr = cerr + 1
hpg = subprocess.check_output(["amixer","-c","0","sset","HP Driver Gain","0"])
clist =  hpg.splitlines()
if clist[5] != "  Front Left: 0 [0%] [-6.00dB]":
    cerr = cerr + 1
if cerr != 0:
    print "CODEC Control Fail"
    error = error + "CODEC Control Fail\n"
'''
subprocess.call(["/home/pi/n7nix/bin/alsa-show.sh"])
print

raw_input("Check GPS sending NMEA sentences ")
subprocess.call(["gpio","-g","write","23","0"]) #turn off LED when done
gerr = 0
nmea = subprocess.check_output(["gpspipe","-r","-n","8"])
nlist =  nmea.splitlines()
del nlist[0:3]
for x in nlist:
    print x
    if x[0:2] != "$G":
        gerr = gerr + 1
        print "ERROR",x
        error = error + "GPS Fail\n"
if gerr == 0:
    print "GPS OK"
print

print "Check PTT LEDs"
raw_input("Left PTT ON ")
subprocess.call(["gpio","-g","write","12","1"])
raw_input("Right PTT ON ")
subprocess.call(["gpio","-g","write","12","0"])
subprocess.call(["gpio","-g","write","23","1"])
print
print error

raw_input("Setup for flash ")
subprocess.call(["gpio","-g","write","23","0"]) #turn off LED when done
subprocess.call(["sudo","cp","config.txt.flash","/boot/config.txt"])
subprocess.call(["sudo","shutdown","now"])
