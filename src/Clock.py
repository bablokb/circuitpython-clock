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

# ESP-01 support
from adafruit_espatcontrol import (
    adafruit_espatcontrol,
    adafruit_espatcontrol_wifimanager,
)

# try to import secrets
try:
  from secrets import secrets
  have_secrets = True
except ImportError:
  have_secrets = False


class Clock:
  """ Helper-class for time """

  # --- constructor   --------------------------------------------------------

  def __init__(self,rtc_ext,rtc_int):
    """ constructor """

    self._rtc_ext = rtc_ext
    self._rtc_int = rtc_int           # internal RTC

    try:
      self._init_esp01();
      print("ESP-01 available")
    except:
      self._wifi = None
      raise

  # --- initialze ESP-01, connect to AP and to remote-port   -----------------

  def _init_esp01(self):
    """ initialize ESP-01 """

    if not have_secrets:
      raise RuntimeError("WiFi settings need the file secrets.py")

    uart = busio.UART(board.TX,board.RX,
                      baudrate=11520,receiver_buffer_size=2048)

    esp = adafruit_espatcontrol.ESP_ATcontrol(
      uart,115200,reset_pin=None,rts_pin=None,debug=secrets['debugflag'])
    self._wifi = adafruit_espatcontrol_wifimanager.ESPAT_WiFiManager(
      esp,secrets,None)

    # try to connect
    retry = secrets['retry']
    while True:
      if retry == 0:
        raise RuntimeError("failed to connect to %s" % secrets['ssid'])
      try:
        self._wifi.connect()
        break
      except Exception as e:
        retry -= 1
        continue

  # --- query local time from time-server   ---------------------------------

  def _get_localtime(self):
    """ query localtime from time-server """

    response = self._wifi.get(TIME_API).json()

    current_time = response["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    year_day = response["day_of_year"]
    week_day = response["day_of_week"]
    is_dst = response["dst"]

    return time.struct_time(
      (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst))

  # --- update local time   -------------------------------------------------

  def update(self,force_net=False):
    """ update internal RTC """

    # force update on:
    #   - explicit request
    #   - external RTC not initialized
    #   - at 03:00 every day

    print("lost_power: %r" % self._rtc_ext.lost_power)
    print("rtc_int: %02d:%02d" %
          (self._rtc_int.datetime.tm_hour,self._rtc_int.datetime.tm_min))
    print("rtc_ext: %02d:%02d" %
          (self._rtc_ext.datetime.tm_hour,self._rtc_ext.datetime.tm_min))
    do_update = (self._wifi and (
      force_net or
      (self._rtc_ext and self._rtc_ext.lost_power) or
      (self._rtc_ext and (self._rtc_ext.datetime.tm_hour == 0 and
                          self._rtc_ext.datetime.tm_min == 0)) or
      (self._rtc_int.datetime.tm_hour == 3 and self._rtc_int.datetime.tm_min == 0))
    )

    try:
      if do_update:
        # update internal+external RTC from internet-time
        print("fetching time from %s" % TIME_API)
        self._rtc_int.datetime = self._get_localtime()
        if self._rtc_ext:
          self._rtc_ext.datetime = self._rtc_int.datetime
        return True
      elif self._rtc_ext:
        # update internal RTC from external RTC
        print("updating from external RTC")
        self._rtc_int.datetime = self._rtc_ext.datetime
        return True
      else:
        # no update-source
        print("no time-source available")
        return False
    except:
      return False
    return True