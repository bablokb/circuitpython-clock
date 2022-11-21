# ----------------------------------------------------------------------------
# wifi_impl_esp32spi.py: Wifi-implementation for ESP32 coprocessor.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import board
import time
import busio
from digitalio import DigitalInOut
from adafruit_esp32spi import adafruit_esp32spi, adafruit_esp32spi_wifimanager

class WifiImpl:
  """ Wifi-implementation for MCU with ESP32 coprocessor """

  # --- constructor   --------------------------------------------------------

  def __init__(self,config,secrets):
    """ constructor """

    self._config  = config
    self._secrets = secrets
    if not hasattr(self._secrets,'channel'):
      self._secrets.channel = 0
    if not hasattr(self._secrets,'timeout'):
      self._secrets.timeout = None

  # --- initialze and connect to AP and to remote-port   ---------------------

  def connect(self):
    """ initialize connection """

    esp32_ready = DigitalInOut(self._config.PIN_ESP_BUSY)
    esp32_gpio0 = DigitalInOut(self._config.PIN_ESP_GPIO0)
    esp32_reset = DigitalInOut(self._config.PIN_ESP_RESET)
    esp32_cs    = DigitalInOut(self._config.PIN_ESP_CS)
    spi         = busio.SPI(self._config.PIN_SCK,
                            self._config.PIN_MOSI, self._config.PIN_MISO)
    esp         = adafruit_esp32spi.ESP_SPIcontrol(
                  spi, esp32_cs, esp32_ready,esp32_reset, esp32_gpio0)

    print("connecting to %s" % self._secrets.ssid)
    try:
      self._wifi  = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(
        esp,
        {'ssid':     self._secrets.ssid,
         'password': self._secrets.password
         },
        None)
    except:
      print("could not connect to %s" % self._secrets.ssid)
      raise

  # --- execute get-request   -----------------------------------------------

  def get(self,url):
    """ process get-request """

    return self._wifi.get(url)

  # --- no specific deep-sleep mode   ---------------------------------------

  def deep_sleep(self):
    """ disable radio """
    pass
