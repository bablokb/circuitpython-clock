A Clock for E-Ink Displays
==========================

**Note: this is work-in-progress. Features and configuration will change in
the future.**

This project implements the software for an e-ink clock using CircuitPython.
The clock displays the current time and is updated every minute. It also
supports the display of temperature and humidity.

Update of date and time uses an attached ESP-01S (unless you use a board
with integrated WLAN like the Magtag or a PicoW). Update occurs at
system startup and once a day. An external RTC is used to keep date/time
in case this update fails.

The software is optimized to minimize battery usage. E.g. you can define
an "active" period during the day when updates take place, otherwise the
clock is left in deep-sleep.


Hardware
--------

You need the following components:

  - a MCU with CircuitPython support
  - an e-ink display
  - an ESP-01S
  - an external RTC
  - a temperature/humidity sensor

Out of the box the software supports:

  - MCU+display: Badger2040 and Magtag
  - RTC: DS3231 and PCF8523
  - AHT20 (for temperature and humidity)

Porting to other hardware should be easy.


Wiring
------

Sensor and RTC use I2C. Connect to Stemma/Qt or respective pins. The ESP-01S
uses UART (RX, TX), a reset-GPIO, 3V3 and GND.

The Magtag only needs the RTC and the sensor. The Badger2040 has suitable
pads on the back for UART, 3V3 and GND. Use the INT-pad for the ESP-01S reset.


Installation
------------

  0. Install the current version of CircuitPython to your device

  1. Install the following libraries from the CircuitPython library-bundle to
     the `lib`-directory of your device  

       - adafruit_ahtx0
       - adafruit_bitmap_font
       - adafruit_bus_device
       - adafruit_display_shapes
       - adafruit_display_text
       - adafruit_ds3231
       - adafruit_espatcontrol
       - adafruit_pcf8523
       - adafruit_register
       - adafruit_requests

     The preferred way to do this is to use `circup` (note that the device
     must be mounted):  

         sudo apt-get -y install pip3
         sudo pip3 install circup
         circup --path /mountpoint/of/device install -r requirements.txt

  2. Clone the repository

  3. Configure the software for your board and preferences. See
     [Configuration](#configuration) below.

  4. Copy all files from below `src` to your device.


Configuration
-------------

For configuration, you need the python-file `settings.py` in the
root-directory of your device. You can find a template in
`template/settings.py'. Copy this file to your device and adapt it to
your needs.

    class Settings:
      pass
    
    settings = Settings()
    secrets  = Settings()
    
    # --- WLAN credentials
    
    secrets.ssid      = 'your_ssid'
    secrets.password  = 'your_password'
    secrets.retry     = 1
    secrets.debugflag = False
    secrets.channel   = 6        # optional
    secrets.timeout   = 10       # optional
    
    # --- update via time-api
    
    settings.TIMEAPI_URL      = "http://worldtimeapi.org/api/ip"
    settings.TIMEAPI_UPD_HOUR = 8
    settings.TIMEAPI_UPD_MIN  = 30
    
    # --- sensor settings
    
    settings.TEMP_OFFSET = 0
    settings.HUM_OFFSET  = 0
    
    # --- active time
    
    #settings.ACTIVE_END_TIME   = "-1:00"           # always active
    settings.ACTIVE_END_TIME    = "22:00"
    #settings.ACTIVE_START_TIME = "07:00"           # start at time-point
    settings.ACTIVE_START_TIME  = None              # start using a button


The first block defines the WLAN credentials. Setting the channel will
speed-up connections, but this only works if your router uses a fixed
channel.

The second block defines the URL of the time-api server and the time of
the regular daily update.

The next block configures offsets for temperature and humidity. No
sensor is perfect and these settings allow some simple calibration.  

The final block defines the active time. If `ACTIVE_START_TIME` is `None`,
the clock enters a deep-sleep with pin-alarm. Magtag and
Badger2040 use the left pin (D15 or SW_A respectively) for this purpose.

If you want the clock to be 100% active, set the end-time to a negative value.
