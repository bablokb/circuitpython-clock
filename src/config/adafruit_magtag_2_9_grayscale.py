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
from configuration import pins

class HWConfig:
  def __init__(self):
    """ constructor """
    self._bat_mon = AnalogIn(board.BATTERY)

  def bat_level(self):
    """ return battery level """
    return (self._bat_mon.value / 65535.0) * 3.3 * 2

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    return alarm.pin.PinAlarm(pins.PIN_ALARM,value=False,edge=False,pull=True)

config = HWConfig()
