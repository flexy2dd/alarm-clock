#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import codecs

from thirdparties.lib_oled96.lib_oled96 import ssd1306
from smbus import SMBus
from PIL import ImageFont, ImageDraw, Image

from modules import constant

# ===========================================================================
# screen Class
# ===========================================================================

class screen():
  
  def __init__(self):
    i2cbus = SMBus(1)            # 1 = Raspberry Pi but NOT early REV1 board
    self.screen = ssd1306(i2cbus)
    self.draw = self.screen.canvas
    
    self.fontSize = 10
    self.width = self.screen.width
    self.height = self.screen.height
    self.rotate = 90
    
    self.screen.onoff(0)

    self.font = ImageFont.truetype('%s/../thirdparties/lib_oled96/FreeSans.ttf' % os.path.dirname(__file__), self.fontSize)
    self.draw.text((0, 0), "Init screen" , font=self.font, fill=1)
    self.screen.display()
    self.screen.onoff(1)
    self.debugLines = []
    
    self.fontSize = 10
    self.maxScreenLines = 6
    
    self.logoWifi100 = Image.open('%s/../icons/wifi-100.png' % os.path.dirname(__file__))
    self.logoWifi75  = Image.open('%s/../icons/wifi-75.png' % os.path.dirname(__file__))
    self.logoWifi50  = Image.open('%s/../icons/wifi-50.png' % os.path.dirname(__file__))
    self.logoWifi25  = Image.open('%s/../icons/wifi-50.png' % os.path.dirname(__file__))
    self.logoWifi0   = Image.open('%s/../icons/wifi-0.png' % os.path.dirname(__file__))
    
  def display(self):
    self.screen.display()
    
  def cls(self, fill = 0):
    self.draw.rectangle((0, 0, self.screen.width-1, self.screen.height-1), outline=0, fill=fill)
    
  def setText(self, left, top, text, fill):
    self.draw.text((left, top), text, font=self.font, fill=fill)
  
  def setRect(self, left, top, width, height, outline, fill):
    self.draw.rectangle((left, top, width, height), outline=outline, fill=fill)
    
  def debug(self, text):
    self.debugLines.append(text)
    linesCount = len(self.debugLines) # how many lines
    
    if (linesCount > self.maxScreenLines):
      self.debugLines.pop(0)
      linesCount = len(self.debugLines)
      
    self.cls()
    for index in range(linesCount):
      iTop = (index * self.fontSize)
      self.draw.text((0, iTop),  self.debugLines[index], font=self.font, fill=1)
    
    self.display()
    
  def viewInfos(self):
    self.cls()
    self.display()
    
  def clock(self):
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second             
    
    font = ImageFont.truetype('%s/../thirdparties/lib_oled96/digital-7mono.ttf' % os.path.dirname(__file__), 55)
    
    self.draw.text((0, 0), now.strftime('%H') , font=font, fill=1)
    self.draw.text((65, 0), now.strftime('%M') , font=font, fill=1)
    
    if ((now.second % 2) == 0): # Toggle colon at 1Hz
      self.draw.text((46, 0), now.strftime(':') , font=font, fill=1)
    
  def alarmInfos(self, bEnable, sNext = ''): 
    font = ImageFont.truetype('%s/../thirdparties/lib_oled96/fontawesome-webfont.ttf' % os.path.dirname(__file__), 12)
    if bEnable:
      text = codecs.unicode_escape_decode(constant.FONT_AWESOME_ICONS["fa-bell-o"])[0]
    else:
      text = codecs.unicode_escape_decode(constant.FONT_AWESOME_ICONS["fa-bell-slash-o"])[0]

    self.draw.text((0, 52), text, font=font, fill=1)
    
    font = ImageFont.truetype('%s/../thirdparties/lib_oled96/FreeSans.ttf' % os.path.dirname(__file__), 12)
    self.draw.text((14, 52), sNext, font=font, fill=1)

  def alarmPlay(self): 
    now = datetime.datetime.now()
    
    font = ImageFont.truetype('%s/../thirdparties/lib_oled96/fontawesome-webfont.ttf' % os.path.dirname(__file__), 60)
    text = codecs.unicode_escape_decode(constant.FONT_AWESOME_ICONS["fa-bell-o"])[0]
    iState = (now.second % 2)
    if self.alarmState==iState:
      return False
    
    if (iState == 0):
      self.cls(1)
      self.draw.text((36, 2), text, font=font, fill=0)
      self.alarmState = 0
    else:
      self.cls(0)
      self.draw.text((36, 2), text, font=font, fill=1)
      self.alarmState = 1
      
    self.display()
    
  def signalLevel(self, level = 0):          
    
    left = 114
    top = 52

    self.draw.rectangle((left, top, left+12, top+14), outline=255, fill=1)

    level = int(level)
    if level>0 and level<=25:
      self.draw.bitmap((left, top), self.logoWifi25, fill=0)
    elif level>25 and level<=50:
      self.draw.bitmap((left, top), self.logoWifi50, fill=0)
    elif level>50 and level<=75:
      self.draw.bitmap((left, top), self.logoWifi75, fill=0)
    elif level>75:
      self.draw.bitmap((left, top), self.logoWifi100, fill=0)
    else:
      self.draw.bitmap((left, top), self.logoWifi0, fill=0)
