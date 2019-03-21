#!/usr/bin/env python
import subprocess

with open('/home/pi/Manufacturing/udrcflash/prodid_4_settings.txt') as f:
    for line in f:
        if line.find('product_ver') != -1:
            print line

raw_input("Flash ")
subprocess.call(["sudo","/home/pi/Manufacturing/udrcflash/flash.sh","4"])

raw_input("Set Up to Test ")
subprocess.call(["sudo","cp","config.txt.test","/boot/config.txt"])
subprocess.call(["sudo","reboot","now"])
