import os
_SYSNAME = os.uname().sysname

from PiicoDev_QMC6310 import *

magnetic_sensor = PiicoDev_QMC6310()

#magnetic_sensor.calibrate()
#stopTheProgram

while True:
     value = magnetic_sensor.read()
     print(value)
     sleep_ms(5)
     polar = magnetic_sensor.readPolar()
     print(polar)
     sleep_ms(5)
     print(magnetic_sensor.readPolarCal())
     print('control registers')
     sleep_ms(5)
     print(magnetic_sensor.getControlRegisters())
     sleep_ms(5)
     print(magnetic_sensor.readTruePolar(declination=12.5))
     sleep_ms(1000)

#    print(magnetic_sensor.readInclination())