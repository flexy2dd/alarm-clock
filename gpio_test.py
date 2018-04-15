#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import re
import argparse
import time
import ConfigParser
import pprint
import datetime
import logging
import logging.handlers

from threading import Timer

from modules import network
from modules import menu
from modules import screen
from modules import constant
from modules import alarm

import RPi.GPIO as GPIO

from PIL import ImageFont, ImageDraw, Image

from thirdparties.adafruit.Adafruit_7Segment import SevenSegment
from thirdparties.lib_oled96.lib_oled96 import ssd1306
from smbus import SMBus

GPIO.setmode(GPIO.BOARD)
GPIO.setup(constant.GPIO_KEY_MENU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_SNOOZE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

clockSegment = SevenSegment(address=0x70)
  
# Continually update the time on a 4 char, 7-segment display
while(True):
  try:
    #print 'GPIO GPIO_KEY_MENU %s' % GPIO.input(constant.GPIO_KEY_MENU)
    #print 'GPIO GPIO_KEY_DOWN %s' % GPIO.input(constant.GPIO_KEY_DOWN)
    #print 'GPIO GPIO_KEY_UP %s' % GPIO.input(constant.GPIO_KEY_UP)

    clockSegment.writeDigit(0, int(GPIO.input(constant.GPIO_KEY_MENU)))
    clockSegment.writeDigit(1, int(GPIO.input(constant.GPIO_KEY_DOWN)))
    clockSegment.writeDigit(3, int(GPIO.input(constant.GPIO_KEY_UP)))
    clockSegment.writeDigit(4, int(GPIO.input(constant.GPIO_KEY_SNOOZE)))

  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise 
