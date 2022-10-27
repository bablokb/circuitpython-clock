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
from wifi_impl_noop import WifiImpl as WifiImpl

class HWConfig:
  def __init__(self):
    """ constructor """
    #self.PIN_TX  = board.TX
    #self.PIN_RX  = board.RX
    #self.PIN_RST = board.INT

  def display(self):
    """ return display """
    return board.DISPLAY

  def bat_level(self):
    """ return battery level """
    return 0.0

config = HWConfig()
