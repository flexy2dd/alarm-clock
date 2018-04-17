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

from thirdparties.lib_oled96.lib_oled96 import ssd1306
from smbus import SMBus

GPIO.setmode(GPIO.BOARD)
GPIO.setup(constant.GPIO_KEY_MENU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_SNOOZE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

gpioKeyMenu = GPIO.input(constant.GPIO_KEY_MENU)
gpioKeyUp = GPIO.input(constant.GPIO_KEY_UP)
gpioKeyDown = GPIO.input(constant.GPIO_KEY_DOWN)
gpioKeySnooze = GPIO.input(constant.GPIO_KEY_SNOOZE)

print('GPIO GPIO_KEY_MENU %s' % gpioKeyMenu)
print('GPIO GPIO_KEY_DOWN %s' % gpioKeyDown)
print('GPIO GPIO_KEY_UP %s' % gpioKeyUp)
print('GPIO GPIO_KEY_SNOOZE %s' % gpioKeySnooze)

# Continually update the time on a 4 char, 7-segment display
while(True):
  try:

    if GPIO.input(constant.GPIO_KEY_MENU) != gpioKeyMenu:
      gpioKeyMenu = GPIO.input(constant.GPIO_KEY_MENU)
      print('GPIO GPIO_KEY_MENU %s' % GPIO.input(constant.GPIO_KEY_MENU))

    if GPIO.input(constant.GPIO_KEY_UP) != gpioKeyUp:
      gpioKeyUp = GPIO.input(constant.GPIO_KEY_UP)
      print('GPIO GPIO_KEY_UP %s' % GPIO.input(constant.GPIO_KEY_UP))

    if GPIO.input(constant.GPIO_KEY_DOWN) != gpioKeyDown:
      gpioKeyDown = GPIO.input(constant.GPIO_KEY_DOWN)
      print('GPIO GPIO_KEY_DOWN %s' % GPIO.input(constant.GPIO_KEY_DOWN))

    if GPIO.input(constant.GPIO_KEY_SNOOZE) != gpioKeySnooze:
      gpioKeySnooze = GPIO.input(constant.GPIO_KEY_SNOOZE)
      print('GPIO GPIO_KEY_SNOOZE %s' % GPIO.input(constant.GPIO_KEY_SNOOZE))


  except:
    print("Unexpected error:", sys.exc_info()[0])
    raise 
