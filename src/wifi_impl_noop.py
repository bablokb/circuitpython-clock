# ----------------------------------------------------------------------------
# wifi_impl_noop.py: dummy Wifi-implementation
#
# Author: Bernhard Bablok
# License: GPL3
#
# Website: https://github.com/bablokb/circuitpython-clock
#
# ----------------------------------------------------------------------------

class WifiImpl:
  """ dummy Wifi-implementation """

  # --- constructor   --------------------------------------------------------

  def __init__(self,config,secrets):
    """ constructor """

    self._config  = config
    self._secrets = secrets

  # --- connect to AP and to remote-port   -----------------------------------

  def connect(self):
    """ initialize and connect """
    raise RuntimeError("connect() not implemented!")

  # --- execute get-request   -----------------------------------------------

  def get(self,url):
    """ process get-request """

    raise RuntimeError("get() not implemented!")

  # --- send ESP01 to deep-sleep   ------------------------------------------

  def deep_sleep(self):
    """ send device to deep-sleep """
    pass
