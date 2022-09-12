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

from Wifi import Wifi

class Clock:
  """ Helper-class for time """

  # --- constructor   --------------------------------------------------------

  def __init__(self,rtc_ext,rtc_int):
    """ constructor """

    self._rtc_ext = rtc_ext
    self._rtc_int = rtc_int           # internal RTC
    self._wifi    = Wifi()

  # --- initialze wifi, connect to AP and to remote-port   -------------------

  def _connect(self):
    """ initialize wifi and connect to AP """

    self._wifi.connect()

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

  # --- send wifi to deep-sleep   -------------------------------------------

  def deep_sleep(self):
    """ send wifi to deep-sleep """

    self._wifi.deep_sleep()

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
        self._wifi.connect()
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
