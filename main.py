import os
_SYSNAME = os.uname().sysname

from PiicoDev_QMC6310 import *

magnetic_sensor = PiicoDev_QMC6310()

while True:
     value = magnetic_sensor.read()
     print(value)
     sleep_ms(1000)
     polar = magnetic_sensor.readPolar()
     print(polar)
     print(magnetic_sensor.readPolarCal())
#     print(magnetic_sensor.getControlRegisters())
     print(magnetic_sensor.readTruePolar(declination=12.5))
#magnetic_sensor.calibrate()
#    print(magnetic_sensor.readInclination())