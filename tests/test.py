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

from modules import network
from modules import menu
from modules import screen
from modules import constant
from modules import alarm

import RPi.GPIO as GPIO

from PIL import ImageFont, ImageDraw, Image

#from thirdparties.adafruit.Adafruit_7Segment import SevenSegment
from thirdparties.lib_oled96.lib_oled96 import ssd1306
from smbus import SMBus

oAlarm = alarm.alarm()

days = ['mon','tue','wed','thu','fri']
#oAlarm.add('7:00', days)
while(True):
  alarmKey = oAlarm.isRun()
  if alarmKey <> False:
    print(alarmKey)
    
  time.sleep(0.25)