#!/usr/bin/env python

import subprocess
import time
import sys
import re

revision = 0.1 #unreleased
print
print "NWDR DRAWS Test Program REV",revision

image = subprocess.check_output(["head","-n 1","/var/log/udr_install.log"])
print image[25:]

error = "Error Report:\n"

print "*** Checking EEPROM"
hat = subprocess.check_output(["ls","/proc/device-tree/"])
if hat.find("hat\n") != -1:
    name = subprocess.check_output(["cat","/proc/device-tree/hat/name"])
    product = subprocess.check_output(["cat","/proc/device-tree/hat/product"])
    product_id = subprocess.check_output(["cat","/proc/device-tree/hat/product_id"])
    product_ver = subprocess.check_output(["cat","/proc/device-tree/hat/product_ver"])
    uuid = subprocess.check_output(["cat","/proc/device-tree/hat/uuid"])
    vendor = subprocess.check_output(["cat","/proc/device-tree/hat/vendor"])
    print "   ",vendor
    print "   ",product
    assy_rev = product_ver[2:4]
    fab_rev = product_ver[5:7]
    print "   ","ASSY Rev",assy_rev,"FAB Rev",fab_rev
else:
    print "!ERROR: DRAWS Not Installed or EEPROM not programmed"
    sys.exit()
print

print "*** Checking /boot/config.txt"
config = subprocess.check_output(["cat","/boot/config.txt"])
conlist = config.splitlines()
print "   ",conlist[-2]
print "   ",conlist[-1]
if (conlist[-1] != "dtoverlay=draws") or (conlist[-2] != "dtoverlay="):
    print "!ERROR: /boot/config.text does not end with:"
    print
    print "dtoverlay="
    print "dtoverlay=draws"
    sys.exit()

print
print "*** Checking Drivers"
drivers = subprocess.check_output(["lsmod"])
#print drivers
if drivers.find("ads1015") != -1:
    print "    ADC: ads1015"
else:
    print "! ads1015 not loaded"
if drivers.find("sc16is7xx") != -1:
    print "    I2C Serial Port: sc16is7xx"
else:
    print "! sc16is7xx not loaded"
if drivers.find("tlv320aic32") != -1: #match overlaps with the next driver re?
    print "    CODEC: tlv320aic32x4"
else:
    print "! tlv320aic32x4 not loaded"
if drivers.find("tlv320aic32x4_i2c") != -1:
    print "    CODEC I2C Control: tlv320aic32x4_i2c"
else:
    print "! tlv320aic32x4_i2c not loaded"
print
print raw_input("***** SW Checks Complete: press return to continue ")

print "*** Checking ADC "
sensors =  subprocess.check_output(["sensors"])
slist =  sensors.splitlines()
print "   ",slist[2]
print "   ",slist[3]
print "   ",slist[4]
print "   ",slist[5]
vstring = slist[3]
vin = float(vstring[24:29])
if (vin < 9) or (vin > 15):
    print "!ERROR Vin out of range (9-15V)"
print

print "*** Checking CODEC "
subprocess.call(["/home/pi/n7nix/bin/alsa-show.sh"])
print

print "*** Checking GPS "
gerr = 0
nmea = subprocess.check_output(["gpspipe","-r","-n","7"])
nlist =  nmea.splitlines()
del nlist[0:3]
for x in nlist:
    print "   ",x
    if x[0:2] != "$G":
        gerr = gerr + 1
        print "ERROR",x
        error = error + "GPS Fail\n"
if gerr != 0:
    print "!ERROR invalid sentences"
print

print "*** Check PTT LEDs return to continue "
subprocess.call(["gpio","-g","write","12","1"])
raw_input("    Left PTT ON return to continue ")
subprocess.call(["gpio","-g","write","12","0"])
subprocess.call(["gpio","-g","write","23","1"])
raw_input("    Right PTT ON return to continue ")
subprocess.call(["gpio","-g","write","23","0"])

print
print error

f = raw_input("f for flash setup ")

if f == "f":
    
    subprocess.call(["sudo","cp","config.txt.flash","/boot/config.txt"])
    subprocess.call(["sudo","shutdown","now"])
