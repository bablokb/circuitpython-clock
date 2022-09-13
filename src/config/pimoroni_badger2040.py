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

class Options:
  pass

config = Options()
config.PIN_TX  = board.TX
config.PIN_RX  = board.RX
config.PIN_RST = board.INT

from wifi_impl_esp01 import WifiImpl as WifiImpl
