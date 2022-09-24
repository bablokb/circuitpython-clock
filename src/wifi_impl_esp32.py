# ----------------------------------------------------------------------------
# wifi_impl_esp32.py: Wifi-implementation for builtin ESP32
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import board
import time
import socketpool
import adafruit_requests

class WifiImpl:
  """ Wifi-implementation for the ESP32 """

  # --- constructor   --------------------------------------------------------

  def __init__(self,config,secrets):
    """ constructor """

    self._config  = config
    self._secrets = secrets
    if not hasattr(self._secrets,'channel'):
      self._secrets['channel'] = 0
    if not hasattr(self._secrets,'timeout'):
      self._secrets['timeout'] = None

  # --- initialze and connect to AP and to remote-port   ---------------------

  def connect(self):
    """ initialize ESP32 """

    import wifi
    print("connecting to %s" % self._secrets["ssid"])
    retries = 3
    while True:
      try:
        wifi.radio.connect(self._secrets["ssid"],
                           self._secrets["password"],
                           channel = self._secrets["channel"],
                           timeout = self._secrets["timeout"]
                           )
        break
      except:
        print("could not connect to %s" % self._secrets["ssid"])
        retries -= 1
        if retries == 0:
          raise
        time.sleep(1)
        continue
    print("connected to %s" % self._secrets["ssid"])
    pool = socketpool.SocketPool(wifi.radio)
    self._requests = adafruit_requests.Session(pool)

  # --- execute get-request   -----------------------------------------------

  def get(self,url):
    """ process get-request """

    return self._requests.get(url)

  # --- no specific deep-sleep mode   ---------------------------------------

  def deep_sleep(self):
    """ disable radio """

    try:                                       # wifi might not be imported
      wifi.radio.enabled = False
    except:
      pass
