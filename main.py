import os
_SYSNAME = os.uname().sysname

from PiicoDev_QMC6310 import *

magnetic_sensor = PiicoDev_QMC6310()

while True:
    value = magnetic_sensor.read()
    print(value)
    sleep_ms(1000)
