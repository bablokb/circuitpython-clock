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

class Options:
  pass

config = Options()
from wifi_impl_esp32 import WifiImpl as WifiImpl

def hw_setup():
  """ setup magtag specific hardware """
  hw_config = Options()
  hw_config.bat_mon = AnalogIn(board.BATTERY)
  return hw_config

def bat_level(hw_conf):
  """ return battery level """
  return (hw_conf.bat_mon.value / 65535.0) * 3.3 * 2
