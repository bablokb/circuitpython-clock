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
try:
  config_file = "/config/"+board.board_id.replace(".","_")
  _temp       = builtins.__import__(config_file,None,None,["config","WifiImpl"],0)
  print("using board-specific implementation")
except:
  config_file = "/config/def_config"
  _temp       = builtins.__import__(config_file,None,None,["config","WifiImpl"],0)
  print("using default implementation")

config      = _temp.config
WifiImpl    = _temp.WifiImpl

# try to import secrets
from settings import secrets
def Wifi():
  return WifiImpl(config,secrets)
