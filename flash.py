#!/usr/bin/env python
import subprocess


subprocess.call(["sudo","Manufacturing/udrcflash/flash.sh","4"])
raw_input("Set Up to Test")
subprocess.call(["sudo","cp","config.txt.flash","/boot/config.txt"])
subprocess.call(["sudo","reboot","now"])
