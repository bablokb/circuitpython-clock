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
from   configuration import secrets, settings

# import board-specific implementation-class
try:
  config_file = "/config/"+board.board_id.replace(".","_")
  cfg         = builtins.__import__(config_file,None,None,["config"],0)
  print("using board-specific implementation")
except:
  config_file = "/config/def_config"
  cfg         = builtins.__import__(config_file,None,None,["config"],0)
  print("using default implementation")

# import wifi-implementation
WifiImpl = builtins.__import__(settings.wifi_module,None,None,["WifiImpl"],0)

def Wifi():
  return WifiImpl.WifiImpl(cfg.config,secrets)
