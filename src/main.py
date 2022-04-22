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

# rtc-support
import adafruit_ds3231

# AHT20
import adafruit_ahtx0
import adafruit_bus_device

# display-support
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

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
      self._rtc = adafruit_ds3231.DS3231(i2c)
    except:
      # use emulation
      self._rtc          = Values()
      self._rtc.datetime = time.struct_time((2022, 4, 22, 13, 12, 47, 4, -1, -1))

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

  # --- update datetime   ----------------------------------------------------

  def update_datetime(self):
    """ read RTC and update values """

    now  = self._rtc.datetime   # this is a struct_time
    time = "{0:02d}:{1:02d}".format(now.tm_hour+2,now.tm_min)
    day  = WDAY[now.tm_wday-1]
    date = "{0:02d}.{1:02d}.{2:02d}".format(now.tm_mday,now.tm_mon,
                                            now.tm_year%100)

    # create time-label and center it
    t = label.Label(FONT_L,text=time,
                    color=BLACK,anchor_point=(0.5,0.5))
    t.anchored_position = (self._display.width/2,self._display.height/2)
    self._group.append(t)

    # additional labels for day and date on the left side
    self.create_text('NW',day)
    self.create_text('NE',date)

  # --- update temperature+humidity   ----------------------------------------

  def update_env_sensor(self):
    """ read sensor and update values """

    self.create_text('SW',"{0:.1f}°C".format(self._sensor.temperature))
    self.create_text('SE',"{0:.0f}%".format(self._sensor.relative_humidity))

  # --- main   ---------------------------------------------------------------

  def run(self):
    self.update_datetime()
    self.update_env_sensor()
    self._display.show(self._group)
    self._display.refresh()

# --- main loop   ------------------------------------------------------------

app = App()
app.run()
while True:
  time.sleep(10)
