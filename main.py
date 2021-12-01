import os
_SYSNAME = os.uname().sysname

from PiicoDev_QMC6310 import *

magnetic_sensor = PiicoDev_QMC6310(odr=3)

#magnetic_sensor.calibrate()
#stopTheProgram

while True:
    value = magnetic_sensor.read()
    print(value)
    sleep_ms(10)
    polar = magnetic_sensor.readPolar()
    print(polar)
    sleep_ms(10)
    print(magnetic_sensor.readPolarCal())
    sleep_ms(10)
    print(magnetic_sensor.readTruePolar(declination=12.5))
    sleep_ms(10)
    print(magnetic_sensor.readMagnitude())
    sleep_ms(10)
    print(magnetic_sensor.readHeading(declination=13.5))
    sleep_ms(1000)
#    print(magnetic_sensor.readInclination())