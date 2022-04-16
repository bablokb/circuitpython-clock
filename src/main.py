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

import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.circle import Circle

FONT_S = bitmap_font.load_font("fonts/DejaVuSans-Bold-24-min.bdf")
FONT_L = bitmap_font.load_font("fonts/DejaVuSans-Bold-52-min.bdf")
BLACK      = 0x000000
WHITE      = 0xFFFFFF

C_OFFSET =  2

class App:

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    self._display = board.DISPLAY
    self._group = displayio.Group()
    self._background()

    self._radius = int((self._display.height-3*C_OFFSET)/4)

    self._map = {
      'NW': (C_OFFSET+self._radius,
             C_OFFSET+self._radius),
      'NE': (self._display.width-C_OFFSET-self._radius,
             C_OFFSET+self._radius),
      'SW': (C_OFFSET+self._radius,
             self._display.height-C_OFFSET-self._radius),
      'SE': (self._display.width-C_OFFSET-self._radius,
             self._display.height-C_OFFSET-self._radius)
    }

  # --- create background   --------------------------------------------------

  def _background(self):
    # white background
    palette    = displayio.Palette(1)
    palette[0] = WHITE 
    background = vectorio.Rectangle(pixel_shader=palette,
                                    width=self._display.width+1,
                                    height=self._display.height, x=0, y=0)
    self._group.append(background)

  # --- create circle with text   --------------------------------------------

  def circle(self,pos,text):
    """ create circle with given text """

    x,y = self._map[pos]
    self._group.append(Circle(x,y,self._radius,fill=WHITE,outline=BLACK))

    t = label.Label(FONT_S,text=text,color=BLACK,
                    anchor_point=(0.5,0.5))
    t.anchored_position = (x,y)
    self._group.append(t)

  # --- update datetime   ----------------------------------------------------

  def update_datetime(self):
    """ read RTC and update values """

    t = label.Label(FONT_L,text="13:22",color=BLACK,
                    anchor_point=(0.5,0.5))
    t.anchored_position = (self._display.width/2,self._display.height/2)
    self._group.append(t)

    day =   '22'
    month = '04'
    self.circle('NW',day)
    self.circle('SW',month)

  # --- update temperature+humidity   ----------------------------------------

  def update_env_sensor(self):
    """ read sensor and update values """

    temp = '20.5°C'
    hum  = '44%'
    self.circle('NE',temp)
    self.circle('SE',hum)

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
