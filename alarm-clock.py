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

# ===========================================================================
# Logging
# ===========================================================================
LOG_FILENAME = "/tmp/alarm-clock.log"
LOG_LEVEL = logging.INFO  # Could be e.g. "DEBUG" or "WARNING"

parser = argparse.ArgumentParser(description="Alarm-clock service")
parser.add_argument("-l", "--log", help="file to write log to (default '" + LOG_FILENAME + "')")
parser.add_argument("-v", "--verbose", help="verbose mode", action='store_true')
parser.add_argument("-s", "--segments", help="view 7 segments clock", action='store_true')

args = parser.parse_args()
if args.log:
  LOG_FILENAME = args.log

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME, when="midnight", backupCount=3)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Make a class we can use to capture stdout and sterr in the log
class oLogger(object):
  def __init__(self, logger, level):
    """Needs a logger and a logger level."""
    self.logger = logger
    self.level = level

  def write(self, message):
    if message.rstrip() != "":
      self.logger.log(self.level, message.rstrip())

if not args.verbose:
  sys.stdout = oLogger(logger, logging.INFO)
  sys.stderr = oLogger(logger, logging.ERROR)

# ===========================================================================
# Menu definition
# ===========================================================================
menu_data = {
  'title': "G�n�ral", 'type': constant.MENU_MENU,
  'options':[
    { 'title': "R�veil", 'type': constant.MENU_COMMAND, 'command': 'setAlarm' },
    { 'title': "Ambiance", 'type': constant.MENU_COMMAND, 'command': 'setAmbiance' },
    { 'title': "Param�tres", 'type': constant.MENU_MENU,
      'options': [
        { 'title': "Informations", 'type': 'viewInfos'},
        { 'title': "Heure", 'type': constant.MENU_COMMAND, 'command': 'setTime' },
        { 'title': "Date", 'type': constant.MENU_COMMAND, 'command': 'setDate' },
      ]
    },
  ]
}

# ===========================================================================
# Clock 
# ===========================================================================
if args.segments:
  clockSegment = SevenSegment(address=0x70)

# ===========================================================================
# Alarm
# ===========================================================================
oAlarm = alarm.alarm()

# ===========================================================================
# Screen
# ===========================================================================
oScreen = screen.screen()

# ===========================================================================
# Button
# ===========================================================================
#GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(constant.GPIO_KEY_MENU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_UP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_DOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(constant.GPIO_KEY_SNOOZE, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def clock():
    tClock = Timer(1.0, clock)
    tClock.start()
    
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second
    # Set hours
    clockSegment.writeDigit(0, int(hour / 10))     # Tens
    clockSegment.writeDigit(1, hour % 10)          # Ones
    # Set minutes
    clockSegment.writeDigit(3, int(minute / 10))   # Tens
    clockSegment.writeDigit(4, minute % 10)        # Ones
    # Toggle colon
    clockSegment.setColon(second % 2)              # Toggle colon at 1Hz
    # Wait a quarter second (less than 1 second to prevent colon blinking getting in phase with odd/even seconds).
    time.sleep(0.25)

oScreen.debug('init clock')

if args.segments:
  clock()

oScreen.debug("ip: %s" % network.get_lan_ip())

# Continually update the time on a 4 char, 7-segment display
while(True):
  try:
    if not (GPIO.input(constant.GPIO_KEY_MENU)):
      print 'Menu'
      menu.processmenu(oScreen, menu_data)
      oScreen.cls()

    # check alarms
    oAlarm.check(oScreen) 
    
    # clear screen
    oScreen.cls()
    
    # add alarm status on screen
    oAlarm.status(oScreen) 
    
    # add clock on screen
    oScreen.clock()
    
    # add wifi level signal on screen
    oScreen.signalLevel(network.get_wifi_signal())
    
    # refresh screen
    oScreen.display()
    
    time.sleep(0.25)
  except:
    print "Unexpected error:", sys.exc_info()[0]
    raise
    
