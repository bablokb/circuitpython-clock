# ----------------------------------------------------------------------------
# main.py: driver program for Clock
#
# This program should work with any board with an integrated display.
# Use settings.py to define your external components:
#   - RTC: e.g. DS3231 or PCF8523
#   - temperatur/humidity: e.g. AHT20
#   - wifi
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import time
start = time.monotonic()

import builtins
import board
import vectorio
import time
import alarm
import rtc

# import board-specific implementations
try:
  config_file = "/config/"+board.board_id.replace(".","_")
  hw_impl = builtins.__import__(config_file,None,None,["config"],0)
  print("using board-specific implementation")
except:
  config_file = "/config/def_config"
  hw_impl = builtins.__import__(config_file,None,None,["config"],0)
  print("using default implementation")

# import settings
from configuration import settings, ui, pins

# display-support
import displayio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font

from Clock import Clock

# --- UI configuration   -----------------------------------------------------

FONT_S   = bitmap_font.load_font("fonts/"+ui.font_s)
FONT_L   = bitmap_font.load_font("fonts/"+ui.font_l)
FG_COLOR = ui.fg_color
BG_COLOR = ui.bg_color
WDAY     = ui.day_names
DATE_FMT = ui.date_fmt

# keep a small gap at the border of the display
GAP =  2

# --- value holder (for emulation)   -----------------------------------------

class Values:
  pass

# --- application class   ----------------------------------------------------

class App:

  # --- constructor   --------------------------------------------------------

  def __init__(self):
    """ constructor """

    # get board-specific implementation and flash LED
    self._hw        = hw_impl.config
    self._hw.led(True)
    time.sleep(getattr(settings,"led_blinktime",0.1))
    self._hw.led(False)

    self._clock  = Clock(settings.rtc_ext(),rtc.RTC())

    # check for power_off pin
    self._check_power_off()

    # initialize display and UI-settings
    self._display   = settings.display()
    width  = self._display.width
    height = self._display.height
    self._map = {
      'NW': ((GAP,       GAP),        (0,0)),
      'NE': ((width-GAP, GAP),        (1,0)),
      'SW': ((GAP,       height-GAP), (0,1)),
      'S':  ((width/2,   height-GAP), (0.5,1)),
      'SE': ((width-GAP, height-GAP), (1,1))
    }

    self._sensor = settings.sensor()

    self._group = displayio.Group()
    self._background()
    self._create_fields()

  # --- check for power-off button press   -----------------------------------

  def _check_power_off(self):
    """ check power_off button """

    # PIN_OFF is a tuple: (pin,active-state), e.g. (board.xx,1)
    if pins.PIN_OFF:
      from digitalio import DigitalInOut, Pull
      off = DigitalInOut(pins.PIN_OFF[0])
      off.pull = Pull.DOWN if pins.PIN_OFF[1] else Pull.UP
      if off.value == pins.PIN_OFF[1]:
        blink_time = getattr(settings,"led_blinktime",0.1)
        for _ in range(3):
          time.sleep(blink_time)
          self._hw.led(True)
          time.sleep(blink_time)
          self._hw.led(False)
        time.sleep(1)                   # extra time for button release
        self._power_off()               # when on battery
        off.deinit()                    # else force deep-sleep
        self.deep_sleep(force=True)
      off.deinit()

  # --- execute power-off if available   -------------------------------------

  def _power_off(self):
    """ power system off """

    if (getattr(settings,"ext_power_on",False) and
        hasattr(settings,"power_off")):
      print("executing power_off()")
      settings.power_off()          # this will only work when on battery

  # --- create background   --------------------------------------------------

  def _background(self):
    """ monochrome background """

    palette    = displayio.Palette(1)
    palette[0] = BG_COLOR
    background = vectorio.Rectangle(pixel_shader=palette,
                                    width=self._display.width+1,
                                    height=self._display.height, x=0, y=0)
    self._group.append(background)

  # --- create text at given location   --------------------------------------

  def _create_text(self,pos,text):
    """ create text at given location """

    t = label.Label(FONT_S,text=text,color=FG_COLOR,
                    anchor_point=self._map[pos][1])
    t.anchored_position = self._map[pos][0]
    self._group.append(t)
    return t

  # --- create text-fields   -------------------------------------------------

  def _create_fields(self):
    """ create text fields for time/sensor """

    # create time-label and center it
    self._time = label.Label(FONT_L,text="00:00",
                             color=FG_COLOR,anchor_point=(0.5,0.5))
    self._time.anchored_position = (self._display.width/2,self._display.height/2)
    self._group.append(self._time)

    # additional labels for day and date on the left side
    self._day = self._create_text('NW',WDAY[0])
    self._date = self._create_text('NE',"01.01.2022")

    if self._sensor:
      # labels for sensor-values
      self._temp = self._create_text('SW',"20.0°C")
      self._hum  = self._create_text('SE',"33%")

    # label for battery-value
    if self._hw.bat_level():
      self._bat  = self._create_text('S',"7.7V")
    else:
      self._bat = None

  # --- query wait-time for inactive period   --------------------------------

  def _get_wait_time(self):
    """ query wait-time in seconds until ACTIVE_TIME_START """

    start_h = int(settings.ACTIVE_START_TIME[0:2])
    start_m = int(settings.ACTIVE_START_TIME[3:5])
    end_h   = int(settings.ACTIVE_END_TIME[0:2])
    end_m   = int(settings.ACTIVE_END_TIME[3:5])

    if not end_h:
      end_h = 24
    if start_h < end_h or start_h == end_h and start_m < end_m:
      start_h += 24

    return ((start_h-end_h-1)*3600 +
            (start_m+60-end_m)*60)

  # --- update datetime   ----------------------------------------------------

  def update_datetime(self):
    """ read RTC and update values """

    now = self._clock.localtime()
    txt_time = "{0:02d}:{1:02d}".format(now.tm_hour,now.tm_min)
    day      = WDAY[now.tm_wday]
    date     = DATE_FMT.format(now.tm_mday,now.tm_mon,
                                               now.tm_year%100)
    self._time.text = txt_time
    self._day.text = day
    self._date.text = date

  # --- update temperature+humidity   ----------------------------------------

  def update_env_sensor(self):
    """ read sensor and update values """

    self._temp.text = "{0:.1f}°C".format(self._sensor.temperature +
                                         settings.TEMP_OFFSET)
    self._hum.text  = "{0:.0f}%".format(self._sensor.relative_humidity +
                                        settings.HUM_OFFSET)

  # --- update battery-level   -----------------------------------------------

  def update_bat_level(self):
    """ query battery level """

    level = self._hw.bat_level()
    self._bat.text = "{0:.1f}V".format(level)

  # --- update   -------------------------------------------------------------

  def update(self):
    """ update time, sensor-values and refresh display """
    self.update_datetime()
    if self._sensor:
      self.update_env_sensor()
    if self._bat:
      self.update_bat_level()
    if hasattr(self._display,"root_group"):
      self._display.root_group = self._group
    else:
      self._display.show(self._group)
    if hasattr(self._display,"time_to_refresh"):
      time.sleep(2*self._display.time_to_refresh)     # Magtag needs this
    self._display.refresh()

  # --- send system to deep-sleep   ------------------------------------------

  def deep_sleep(self,force=False):
    """ send system to deep-sleep """

    now = time.localtime()
    self._clock.deep_sleep()

    # check for long sleep during inactive period (e.g. at night)
    if force or (now.tm_hour == int(settings.ACTIVE_END_TIME[0:2]) and
        now.tm_min  == int(settings.ACTIVE_END_TIME[3:5])):
      print("end of active time, taking a long nap")
      if settings.ACTIVE_START_TIME:
        wait_time = self._get_wait_time()
      else:
        self._power_off()                   # when on battery
        pin_alarm = self._hw.pin_alarm()    # else normal pin-alarm
        if pin_alarm:
          print("deep-sleep until button-press")
          if settings.deep_sleep:
            alarm.exit_and_deep_sleep_until_alarms(pin_alarm)
          else:
            alarm.light_sleep_until_alarms(pin_alarm)
            return
        else:
          raise Exception("error: no alarm-button configured")
    else:
      # wake up at next full minute
      wait_time  = 60 - now.tm_sec

    alarm_time = time.mktime(now) + wait_time
    print("deep-sleep for %d seconds" % wait_time)

    # check if we just sleep or use an external rtc for wakeup.
    # On a pico, the pin-alarm is far more efficient than the timer-alarm,
    # so this saves considerable power
    if (hasattr(settings,"rtc_ext_wakeup") and pins.RTC_ALARM and
        self._clock.set_alarm(alarm_time)):
      print("using PinAlarm from external RTC")
      wake_alarm = alarm.pin.PinAlarm(pins.RTC_ALARM,
                                      value=settings.rtc_ext_wakeup,
                                      edge=True,pull=True)
    else:
      print("using TimeAlarm from internal RTC")
      wake_alarm = alarm.time.TimeAlarm(epoch_time=alarm_time)
    if settings.deep_sleep:
      self._power_off()                                   # when on battery
      alarm.exit_and_deep_sleep_until_alarms(wake_alarm)  # else deep-sleep
    else:
      alarm.light_sleep_until_alarms(wake_alarm)

# --- main loop   ------------------------------------------------------------

app = App()
print("startup: %f s" % (time.monotonic()-start))
while True:
  start = time.monotonic()
  app.update()
  print("update: %fs" % (time.monotonic()-start))
  app.deep_sleep()
