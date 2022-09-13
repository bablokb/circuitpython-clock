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
import busio
from   digitalio import DigitalInOut

# import board-specific implementation-class
config_file = "/config/"+board.board_id.replace(".","_")
_temp       = builtins.__import__(config_file,None,None,["config","WifiImpl"],0)
config      = _temp.config
WifiImpl    = _temp.WifiImpl

# try to import secrets
try:
  from secrets import secrets
except ImportError:
  raise RuntimeError("WiFi settings need the file secrets.py")

def Wifi():
  return WifiImpl(config,secrets)
