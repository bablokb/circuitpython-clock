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
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

class Options:
  pass

config = Options()
config.PIN_TX  = board.TX
config.PIN_RX  = board.RX
config.PIN_RST = board.INT

from wifi_impl_esp01 import WifiImpl as WifiImpl

def hw_setup():
  """ setup Badger2040 specific hardware """
  hw_config = Options()
  hw_config.bat_mon = AnalogIn(board.VBAT_SENSE)
  hw_config.ref_1V2 = AnalogIn(board.REF_1V2)
  hw_config.ref_pow = DigitalInOut(board.VREF_POWER)
  hw_config.ref_pow.direction = Direction.OUTPUT
  return hw_config

def bat_level(hw_conf):
  """ return battery level """
  hw_conf.ref_pow.value = 1
  vdd   = 1.24*65535/hw_conf.ref_1V2.value
  level = hw_conf.bat_mon.value/65535*vdd*3
  hw_conf.ref_pow.value = 0
  return level
