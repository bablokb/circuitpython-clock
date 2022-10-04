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
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction

class Options:
  pass

config = Options()
#config.PIN_TX  = board.TX
#config.PIN_RX  = board.RX 
#config.PIN_RST = board.XXX

from wifi_impl_noop import WifiImpl as WifiImpl

def hw_setup():
  """ setup specific hardware """
  hw_config = Options()
  return hw_config

def bat_level(hw_conf):
  """ return battery level """
  return 0.0
