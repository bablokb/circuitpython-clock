# ----------------------------------------------------------------------------
# Wifi.py: Manage wifi-setup and requests
#
# The code is a bit tricky: it delegates the implementation of Wifi
# to a second class which in turn is loaded from a board-specific
# file. Please check the files in /config.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import builtins
import board
from   configuration import secrets, settings, pins

# import wifi-implementation
if settings.wifi_module:
  WifiImpl = builtins.__import__(settings.wifi_module,None,None,["WifiImpl"],0)
  def Wifi():
    return WifiImpl.WifiImpl(pins,secrets)
