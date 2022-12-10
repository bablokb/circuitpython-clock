# ----------------------------------------------------------------------------
# template/configuration.py: runtime configuration settings template for
# a Pico-W with a Pimoroni Pico Inky Pack display.
#
# This can be used as a blueprint for setups with non-builtin displays.
#
# Adapt to your needs (credentials, active-time, hardware, ui).
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

import board
import adafruit_pcf8523        # PCF8523 support
#import adafruit_ds3231        # DS3231 support
import adafruit_ahtx0          # AHT20
import adafruit_bus_device

# for Pimoroni Inky-Pack e-paper display
import busio
import displayio
import InkyPack

class Settings:
  pass

# --- some containers ---

settings = Settings()
secrets  = Settings()
pins     = Settings()
ui       = Settings()

# --- WLAN credentials ---

secrets.ssid      = 'your_ssid'
secrets.password  = 'your_password'
secrets.retry     = 1
secrets.debugflag = False
secrets.channel   = 6        # optional
secrets.timeout   = 10       # optional

# --- update via time-api ---

settings.TIMEAPI_URL      = "http://worldtimeapi.org/api/ip"
settings.TIMEAPI_UPD_HOUR = 8
settings.TIMEAPI_UPD_MIN  = 30

# --- sensor settings ---

settings.TEMP_OFFSET = 0
settings.HUM_OFFSET  = 0

# --- active time ---

#settings.ACTIVE_END_TIME   = "-1:00"           # always active
settings.ACTIVE_END_TIME    = "22:00"
#settings.ACTIVE_START_TIME = "07:00"           # start at time-point
settings.ACTIVE_START_TIME  = None              # start using a button

# --- helper-function for non-builtin-displays ---

def create_display():
  displayio.release_displays()

  # pinout for Pimoroni Inky Pack
  SCK_PIN  = board.GP18
  MOSI_PIN = board.GP19
  MISO_PIN = board.GP16
  CS_PIN   = board.GP17
  RST_PIN  = board.GP21
  DC_PIN   = board.GP20
  BUSY_PIN = board.GP26

  spi = busio.SPI(SCK_PIN,MOSI=MOSI_PIN,MISO=MISO_PIN)
  display_bus = displayio.FourWire(
      spi, command=DC_PIN, chip_select=CS_PIN, reset=RST_PIN, baudrate=1000000
  )
  return InkyPack.InkyPack(display_bus,busy_pin=BUSY_PIN)

# --- hardware-setup ---

i2c = busio.I2C(board.GP3,board.GP2)
settings.display = create_display               # create-method
settings.deep_sleep = True                      # use deep-sleep
#settings.deep_sleep = False                    # for non-epaper displays

#settings.rtc_ext = lambda: None                # no external RTC
settings.rtc_ext = lambda: adafruit_pcf8523.PCF8523(i2c)
#settings.rtc_ext = lambda: adafruit_ds3231.DS3231(i2c)

#settings.sensor = lambda: None                 # no temp/humidity sensor
settings.sensor = lambda: adafruit_ahtx0.AHTx0(i2c)

#settings.wifi_module = None                    # no WIFI
#settings.wifi_module = "wifi_impl_esp01"        # implementing module
#settings.wifi_module = "wifi_impl_esp32spi"    # implementing module
settings.wifi_module = "wifi_impl_builtin"     # implementing module

# --- pins ---

pins.PIN_ALARM = board.GP12                     # wakeup pin (SW_A)

# --- UI ---

ui.bg_color  = 0xFFFFFF                         # white
ui.fg_color  = 0x000000                         # black
ui.font_s    = "DejaVuSans-Bold-24-min.bdf"     # small font
ui.font_l    = "DejaVuSans-Bold-52-min.bdf"     # large font
ui.day_names = {
  0: 'Montag',      1: 'Dienstag',  2: 'Mittwoch',
  3: 'Donnerstag',  4: 'Freitag',   5: 'Samstag',  6: 'Sonntag'
  }
ui.date_fmt  = "{0:02d}.{1:02d}.{2:02d}"        # dd.mm.yy

#ui.day_names = {
#  0: 'Monday',      1: 'Tuesday',   2: 'Wednesday',
#  3: 'Thursday',    4: 'Friday',    5: 'Saturday',  6: 'Sunday'
#  }
#ui.date_fmt  = "{1:02d}/{0:02d}/{2:02d}"       # mm/dd/yy
