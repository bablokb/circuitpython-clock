# ----------------------------------------------------------------------------
# pimoroni_badger2040w.py: board-specific setup for Badger2040W
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
    pass

  def bat_level(self):
    """ return battery level """
    adc = AnalogIn(board.VOLTAGE_MONITOR)
    level = adc.value *  3 * 3.3 / 65535
    adc.deinit()
    return level

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    return alarm.pin.PinAlarm(pins.PIN_ALARM,value=True,edge=True,pull=True)

config = HWConfig()
