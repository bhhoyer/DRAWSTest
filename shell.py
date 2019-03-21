#!/usr/bin/env python

#import sh

with open('/home/pi/Manufacturing/udrcflash/prodid_4_settings.txt') as f:
    for line in f:
        if line.find('product_ver') != -1:
            print line