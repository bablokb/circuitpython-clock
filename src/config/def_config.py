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
    return 0.0

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    return alarm.pin.PinAlarm(pins.PIN_ALARM,value=False,edge=True,pull=True)

config = HWConfig()
