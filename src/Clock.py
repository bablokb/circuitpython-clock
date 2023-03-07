# ----------------------------------------------------------------------------
# Clock.py: Wrapper for current (local) time.
#
# This class keeps and updates time from three sources:
#   - the internal RTC
#   - an external RTC
#   - internet (e.g. from worldtimeapi.org)
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

MEM_RTC_STATE = 0
MEM_API_STATE = 1

import time
import alarm
import microcontroller
from configuration import settings

class Clock:
  """ Helper-class for time """

  # --- constructor   --------------------------------------------------------

  def __init__(self,rtc_ext,rtc_int):
    """ constructor """

    self._rtc_ext = rtc_ext
    self._rtc_int = rtc_int           # internal RTC
    self._wifi    = None
    try:
      if alarm.sleep_memory:
        print("using sleep-memory for status")
        self._mem = alarm.sleep_memory
      else:
        print("using nvram for status")
        self._mem = microcontroller.nvm
    except:
      print("using nvram for status")
      self._mem = microcontroller.nvm

    # clear any alarms
    if hasattr(settings,"rtc_ext_wakeup"):
      if hasattr(self._rtc_ext,"alarm1"):
        self._rtc_ext.alarm1_status = False
        print("clearing alarm1")
      elif hasattr(self._rtc_ext,"alarm"):
        self._rtc_ext.alarm_status = False
        print("clearing alarm")

  # --- initialze wifi, connect to AP and to remote-port   -------------------

  def _connect(self):
    """ initialize wifi and connect to AP """

    from Wifi import Wifi
    self._wifi = Wifi()
    self._wifi.connect()

  # --- query local time from time-server   ---------------------------------

  def _get_remotetime(self):
    """ query time from time-server """

    response = self._wifi.get(settings.TIMEAPI_URL).json()

    if 'struct_time' in response:
      return time.struct_time(tuple(response['struct_time']))

    current_time = response["datetime"]
    the_date, the_time = current_time.split("T")
    year, month, mday = [int(x) for x in the_date.split("-")]
    the_time = the_time.split(".")[0]
    hours, minutes, seconds = [int(x) for x in the_time.split(":")]

    year_day = int(response["day_of_year"])
    week_day = int(response["day_of_week"])
    week_day = 6 if week_day == 0 else week_day-1
    is_dst   = int(response["dst"])

    return time.struct_time(
      (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst))

  # --- check state of external RTC   ---------------------------------------

  def _check_rtc(self,rtc):
    """ check if RTC has a technically valid time """

    if not rtc:
      return False

    ts = rtc.datetime
    return (ts.tm_year > 2021 and ts.tm_mon < 13 and ts.tm_mday < 32 and
            ts.tm_hour < 25   and ts.tm_min < 60 and ts.tm_sec   < 60)

  # --- set state of external RTC   -----------------------------------------

  def _set_rtc_state(self,ts):
    """ set state of external RTC """

    if ts:
      print("updated RTCs from %s" % settings.TIMEAPI_URL)
      self._rtc_int.datetime = ts
      if self._rtc_ext:
        self._rtc_ext.datetime = ts
        if self._mem[MEM_RTC_STATE] != 1:
          self._mem[MEM_RTC_STATE] = 1
    else:
      state = self._mem[MEM_RTC_STATE] == 1 and self._check_rtc(self._rtc_ext)
      if state:
        # external RTC claims to be valid and passes the heuristic check
        print("using external RTC")
        ext_ts = self._rtc_ext.datetime
        self._rtc_int.datetime = ext_ts
      elif self._mem[MEM_RTC_STATE] == 1:
        # invalid value of external RTC
        print("using internal RTC, clearing ext RTC-state")
        self._mem[MEM_RTC_STATE] = 0
      elif self._rtc_ext:
        print("using internal RTC, setting external RTC from internal")
        int_ts = self._rtc_int.datetime          # a valid ext. RTC will allow
        self._rtc_ext.datetime = int_ts          # us to use RTC-alarms
      else:
        print("using internal RTC")

  # --- send wifi to deep-sleep   -------------------------------------------

  def deep_sleep(self):
    """ send wifi to deep-sleep """

    if self._wifi:
      self._wifi.deep_sleep()

  # --- set alarm-time   ----------------------------------------------------

  def set_alarm(self,alarm_time):
    """ set alarm-time. DS3231 has alarm1, while PCF85x3 has alarm """

    if self._rtc_ext:
      if hasattr(self._rtc_ext,"clockout_enabled"):
        self._rtc_ext.clockout_enabled = False
      elif hasattr(self._rtc_ext,"clockout_frequency"):
        self._rtc_ext.clockout_frequency = 0b111
      if hasattr(self._rtc_ext,"alarm1"):
        self._rtc_ext.alarm1  = (time.localtime(alarm_time),"daily")
        self._rtc_ext.alarm1_interrupt = True
        return True
      elif hasattr(self._rtc_ext,"alarm"):
        self._rtc_ext.alarm  = (time.localtime(alarm_time),"daily")
        self._rtc_ext.alarm_interrupt = True
        return True
      else:
        return False
    else:
      return False

  # --- return local time   -------------------------------------------------

  def localtime(self,force_upd=False):
    """ return localtime, updating RTCs if necessary """

    print("rtc_int:    %02d:%02d %02d.%02d.%04d" %
          (self._rtc_int.datetime.tm_hour,self._rtc_int.datetime.tm_min,
           self._rtc_int.datetime.tm_mday,self._rtc_int.datetime.tm_mon,
           self._rtc_int.datetime.tm_year))
    if self._rtc_ext:
      print("rtc_ext:    %02d:%02d %02d.%02d.%04d" %
            (self._rtc_ext.datetime.tm_hour,self._rtc_ext.datetime.tm_min,
             self._rtc_ext.datetime.tm_mday,self._rtc_ext.datetime.tm_mon,
             self._rtc_ext.datetime.tm_year))
    else:
      print("rtc_ext: not available")
    print("RTC-state:  %d" % self._mem[MEM_RTC_STATE])
    print("API-state:  %d" % self._mem[MEM_API_STATE])

    do_update = (
      force_upd or                             # explicit request
      (self._rtc_ext and
        self._mem[MEM_RTC_STATE] != 1 ) or     # external RTC not valid
      (not self._rtc_ext and not               # no external RTC, so
       self._check_rtc(self._rtc_int)) or      #   check internal rtc
      self._mem[MEM_API_STATE] != 1            # last API-call not valid
    )
    do_update_daily = (
      self._rtc_int.datetime.tm_hour == settings.TIMEAPI_UPD_HOUR and
      self._rtc_int.datetime.tm_min == settings.TIMEAPI_UPD_MIN
    )

    if settings.wifi_module and (do_update or do_update_daily):
      try:
        self._connect()
        # update internal+external RTC from internet-time
        print("fetching time from %s" % settings.TIMEAPI_URL)
        ts = self._get_remotetime()
        self._set_rtc_state(ts)
        if self._mem[MEM_API_STATE] != 1:
          self._mem[MEM_API_STATE] = 1
      except Exception as ex:
        # no internet-connection or time-api fails
        print("exception fetching time: %r" % ex)
        self._set_rtc_state(None)
        if self._mem[MEM_API_STATE] == 1 and do_update:
          # a failing daily update alone should not trigger new updates
          self._mem[MEM_API_STATE] = 0
    else:
      self._set_rtc_state(None)
    return time.localtime()
