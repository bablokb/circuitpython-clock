# ----------------------------------------------------------------------------
# adafruit_magtag_2_9_grayscale.py: board-specific setup for Magtag
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import board
from analogio import AnalogIn

from wifi_impl_esp32 import WifiImpl as WifiImpl

class HWConfig:
  def __init__(self):
    """ constructor """
    self._bat_mon = AnalogIn(board.BATTERY)

  def display(self):
    """ return display """
    return board.DISPLAY

  def bat_level(self):
    """ return battery level """
    return (self._bat_mon.value / 65535.0) * 3.3 * 2

config = HWConfig()
