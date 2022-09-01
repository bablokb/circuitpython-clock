# ----------------------------------------------------------------------------
# Clock.py: Maintain time using ESP-01 and/or external RTC.
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-badger-clock
#
# ----------------------------------------------------------------------------

TIME_API  = "http://worldtimeapi.org/api/ip"

import board
import busio
import time
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

class Clock:
  """ Helper-class for time """

  # --- constructor   --------------------------------------------------------

  def __init__(self,rtc_ext,rtc_int):
    """ constructor """

    self._rtc_ext = rtc_ext
    self._rtc_int = rtc_int           # internal RTC
    self._esp     = None

  # --- initialze ESP-01, connect to AP and to remote-port   -----------------

  def _init_esp01(self):
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

  # --- query local time from time-server   ---------------------------------

  def _get_remotetime(self):
    """ query time from time-server """

    response = self._wifi.get(TIME_API).json()

    current_time = response["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    year_day = int(response["day_of_year"])
    week_day = int(response["day_of_week"]) - 1
    is_dst   = int(response["dst"])

    return time.struct_time(
      (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst))

  # --- send ESP01 to deep-sleep   ------------------------------------------

  def deep_sleep(self):
    """ send ESP01 to deep-sleep """

    if self._esp:
      self._esp.deep_sleep(0)

  # --- return local time   -------------------------------------------------

  def localtime(self,force_net=False):
    """ return localtime, updating RTCs if necessary """

    # force update on:
    #   - explicit request
    #   - external RTC not initialized
    #   - at 03:00 every day

    print("lost_power: %r" % self._rtc_ext.lost_power)
    print("rtc_int: %02d:%02d" %
          (self._rtc_int.datetime.tm_hour,self._rtc_int.datetime.tm_min))
    print("rtc_ext: %02d:%02d" %
          (self._rtc_ext.datetime.tm_hour,self._rtc_ext.datetime.tm_min))

    do_update = (
      force_net or self._rtc_ext.lost_power or
      (self._rtc_ext.datetime.tm_hour == 0 and
                          self._rtc_ext.datetime.tm_min == 0) or
      (self._rtc_int.datetime.tm_hour == 3 and self._rtc_int.datetime.tm_min == 0)
    )

    if do_update:
      try:
        self._init_esp01()
        # update internal+external RTC from internet-time
        print("fetching time from %s" % TIME_API)
        ts = self._get_remotetime()               # N.B.: this is (!!)
        self._rtc_int.datetime = ts               # necessary
        self._rtc_ext.datetime = ts
      except Exception as ex:
        # no internet-connection
        print("exception: %r" % ex)
        print("falling back to external RTC")
        ts = self._rtc_ext.datetime
        self._rtc_int.datetime = ts
    elif self._rtc_int.datetime.tm_hour == 0 and self._rtc_int.datetime.tm_min < 2:
      # update int from ext
      print("using external RTC")
      ts = self._rtc_ext.datetime
      self._rtc_int.datetime = ts
    else:
      # no update, just return localtime
      print("using internal RTC")
    return time.localtime()
