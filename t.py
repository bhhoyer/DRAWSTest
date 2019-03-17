#!/usr/bin/env python

import subprocess
import time

subprocess.call(["n7nix/bin/udrcver.sh"])
raw_input("")
subprocess.call(["sensors"])
raw_input("")
subprocess.call(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","10 kOhm"])
subprocess.call(["amixer","-c","0","sset","CM_L to Left Mixer Negative Resistor","40 kOhm"])
raw_input("")
subprocess.call(["gpsmon"])
raw_input("")
subprocess.call(["sudo","shutdown","now"])
