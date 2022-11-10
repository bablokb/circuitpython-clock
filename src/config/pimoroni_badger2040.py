# ----------------------------------------------------------------------------
# pimoroni_badger2040.py: board-specific setup for Badger2040
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
from digitalio import DigitalInOut, Direction
from wifi_impl_esp01 import WifiImpl as WifiImpl

class HWConfig:
  def __init__(self):
    """ constructor """
    self.PIN_TX  = board.TX
    self.PIN_RX  = board.RX
    self.PIN_RST = board.INT

    self._bat_mon = AnalogIn(board.VBAT_SENSE)
    self._ref_1V2 = AnalogIn(board.REF_1V2)
    self._ref_pow = DigitalInOut(board.VREF_POWER)
    self._ref_pow.direction = Direction.OUTPUT

  def bat_level(self):
    """ return battery level """
    self._ref_pow.value = 1
    vdd   = 1.24*65535/self._ref_1V2.value
    level = self._bat_mon.value/65535*vdd*3
    self._ref_pow.value = 0
    return level

  def pin_alarm(self):
    """ return pre-configured pin-alarm """
    return alarm.pin.PinAlarm(board.SW_A,value=True,edge=True,pull=True)

config = HWConfig()
