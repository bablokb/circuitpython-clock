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
