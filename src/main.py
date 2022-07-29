# ----------------------------------------------------------------------------
# main.py: driver program for Badger-Clock
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-badger-clock
#
# ----------------------------------------------------------------------------

import board
import vectorio
import time
import alarm
import rtc

# DS3231 support
import adafruit_ds3231

# AHT20
import adafruit_ahtx0
import adafruit_bus_device

# display-support
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from Clock import Clock

# fonts and colors
FONT_S = bitmap_font.load_font("fonts/DejaVuSans-Bold-24-min.bdf")
FONT_L = bitmap_font.load_font("fonts/DejaVuSans-Bold-52-min.bdf")
BLACK      = 0x000000
WHITE      = 0xFFFFFF

# keep a small gap at the border of the display
GAP =  2

# map wday-numbers to names of day
WDAY = {
  0: 'Montag',      1: 'Dienstag',  2: 'Mittwoch',
  3: 'Donnerstag',  4: 'Freitag',   5: 'Samstag',  6: 'Sonntag'
  }

# --- value holder (for emulation)   -----------------------------------------

class Values:
  pass

# --- application class   ----------------------------------------------------

class App:

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._display = board.DISPLAY
    self._group = displayio.Group()
    self._background()

    self._time = None
    self._day  = None
    self._date = None
    self._temp = None
    self._hum  = None

    width  = self._display.width
    height = self._display.height
    self._map = {
      'NW': ((GAP,       GAP),        (0,0)),
      'NE': ((width-GAP, GAP),        (1,0)),
      'SW': ((GAP,       height-GAP), (0,1)),
      'SE': ((width-GAP, height-GAP), (1,1))
    }

    i2c = board.I2C()
    try:
      rtc_ext = adafruit_ds3231.DS3231(i2c)
      print("using DS3231")
    except:
      try:
        rtc_ext = ...
        print("using ")
      except:
        rtc_ext = Values()
        rtc_ext.datetime = time.struct_time((2022, 4, 22, 13, 12, 47, 4, -1, -1))
        print("emulating external RTC")

    self._clock = Clock(rtc_ext,rtc.RTC())
    self._clock.update()

    try:
      self._sensor = adafruit_ahtx0.AHTx0(i2c)
    except:
      # use emulation
      self._sensor                   = Values()
      self._sensor.temperature       = 22.5
      self._sensor.relative_humidity = 44

  # --- create background   --------------------------------------------------

  def _background(self):
    """ all white background """

    palette    = displayio.Palette(1)
    palette[0] = WHITE 
    background = vectorio.Rectangle(pixel_shader=palette,
                                    width=self._display.width+1,
                                    height=self._display.height, x=0, y=0)
    self._group.append(background)

  # --- create text at given location   --------------------------------------

  def create_text(self,pos,text):
    """ create text at given location """

    t = label.Label(FONT_S,text=text,color=BLACK,
                    anchor_point=self._map[pos][1])
    t.anchored_position = self._map[pos][0]
    self._group.append(t)
    return t

  # --- update datetime   ----------------------------------------------------

  def update_datetime(self):
    """ read RTC and update values """

    now      = time.localtime()
    txt_time = "{0:02d}:{1:02d}".format(now.tm_hour,now.tm_min)
    day      = WDAY[now.tm_wday]
    date     = "{0:02d}.{1:02d}.{2:02d}".format(now.tm_mday,now.tm_mon,
                                               now.tm_year%100)

    if not self._time:
      # create time-label and center it
      self._time = label.Label(FONT_L,text=txt_time,
                      color=BLACK,anchor_point=(0.5,0.5))
      self._time.anchored_position = (self._display.width/2,self._display.height/2)
      self._group.append(self._time)
    else:
      self._time.text = txt_time

    # additional labels for day and date on the left side
    if not self._day:
      self._day = self.create_text('NW',day)
    else:
      self._day.text = day

    if not self._date:
      self._date = self.create_text('NE',date)
    else:
      self._date.text = date

  # --- update temperature+humidity   ----------------------------------------

  def update_env_sensor(self):
    """ read sensor and update values """

    temp = "{0:.1f}°C".format(self._sensor.temperature)
    if not self._temp:
      self._temp = self.create_text('SW',temp)
    else:
      self._temp.text = temp

    hum = "{0:.0f}%".format(self._sensor.relative_humidity)
    if not self._hum:
      self._hum = self.create_text('SE',hum)
    else:
      self._hum.text = hum

  # --- update   -------------------------------------------------------------

  def update(self):
    self.update_datetime()
    self.update_env_sensor()
    self._display.show(self._group)
    self._display.refresh()

# --- main loop   ------------------------------------------------------------

app = App()

while True:
  app.update()
  now = time.localtime()
  w_time = 60 - now.tm_sec
  print("waiting for %d seconds" % w_time)
  wake_alarm = alarm.time.TimeAlarm(monotonic_time=time.monotonic()+w_time)
  #alarm.light_sleep_until_alarms(wake_alarm)
  #alarm.exit_and_deep_sleep_until_alarms(wake_alarm)
  time.sleep(w_time)
