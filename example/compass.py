# compass
from PiicoDev_QMC6310 import *

magnetometer = PiicoDev_QMC6310()

magnetometer.calibrate()

while True:
    heading = magnetometer.readHeading()
    print(heading)
    sleep_ms(1000)