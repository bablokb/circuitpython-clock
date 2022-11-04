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

For configuration, you need two python-files in the root-directory
of your device:

  - `secrets.py`: here you configure your SSID and WLAN-password

         secrets = {
           'ssid' : 'my-ssid',
           'password' : 'my-password',
           'retry': 1,
           'debugflag': False
         }

  - `settings.py`: here you can configure various aspects of the software.
     The first block deals with updates of the local-time. In the example
     time is updated at 08:30 every day.  
     The second block configures offsets for temperature and humidity. No
     sensor is perfect and these settings allow some simple calibration.  
     The third block defines the active time. If `ACTIVE_START_TIME` is `None`,
     the clock enters a deep-sleep with pin-alarm. For Magtag and
     Badger2040 the left pin (D15 or SW_A respectively) serves as the
     wakeup-pin.

         TIMEAPI_URL      = "http://worldtimeapi.org/api/ip"
         TIMEAPI_UPD_HOUR = 8
         TIMEAPI_UPD_MIN  = 30
     
         TEMP_OFFSET = -0.3
         HUM_OFFSET  = -3
     
         ACTIVE_END_TIME   = "22:00"
         #ACTIVE_START_TIME = "07:00"
         ACTIVE_START_TIME = None
