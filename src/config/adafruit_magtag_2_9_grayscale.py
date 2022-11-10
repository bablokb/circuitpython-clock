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
import alarm
from analogio import AnalogIn

from wifi_impl_esp32 import WifiImpl as WifiImpl

class HWConfig:
  def __init__(self):
    """ constructor """
    self._bat_mon = AnalogIn(board.BATTERY)

  def bat_level(self):
    """ return battery level """
    return (self._bat_mon.value / 65535.0) * 3.3 * 2

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    return alarm.pin.PinAlarm(board.D15,value=False,edge=False,pull=True)

config = HWConfig()
