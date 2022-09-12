# ----------------------------------------------------------------------------
# Wifi.py: Manage wifi-setup and requests
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-badger-clock
#
# ----------------------------------------------------------------------------

import board
import busio
from   digitalio import DigitalInOut

# ESP-01 support
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)

# try to import secrets
try:
  from secrets import secrets
except ImportError:
  raise RuntimeError("WiFi settings need the file secrets.py")

class Wifi:
  """ Wrapper for wifi-implementation """

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    self._esp     = None

  # --- initialze ESP-01, connect to AP and to remote-port   -----------------

  def connect(self):
    """ initialize ESP-01 """

    uart = busio.UART(board.TX,board.RX,
                      baudrate=11520,receiver_buffer_size=2048)

    rst_pin = DigitalInOut(board.INT)
    self._esp = adafruit_espatcontrol.ESP_ATcontrol(
      uart,115200,reset_pin=rst_pin,rts_pin=None,debug=secrets['debugflag'])

    self._wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(
      self._esp,secrets,None,secrets['retry'])

    # try to connect
    try:
      print("trying to connect...",end='')
      self._wifi.connect()
      print("...done")
    except Exception as e:
      print("...failed: %r" % e)
      raise RuntimeError("failed to connect to %s" % secrets['ssid'])

  # --- execute get-request   -----------------------------------------------

  def get(self,url):
    """ process get-request """

    return self._wifi.get(url)

  # --- send ESP01 to deep-sleep   ------------------------------------------

  def deep_sleep(self):
    """ send ESP01 to deep-sleep """

    if self._esp:
      self._esp.deep_sleep(0)

