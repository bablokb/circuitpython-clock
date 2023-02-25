# ----------------------------------------------------------------------------
# def_config.py: default for board-specific setup
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
    if hasattr(board,"VOLTAGE_MONITOR"):
      adc = AnalogIn(board.VOLTAGE_MONITOR)
      level = adc.value *  3 * 3.3 / 65535
      adc.deinit()
      return level
    else:
      return 0.0

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    if pins.PIN_ALARM:
      return alarm.pin.PinAlarm(pins.PIN_ALARM,value=False,edge=True,pull=True)
    else:
      return None

config = HWConfig()
