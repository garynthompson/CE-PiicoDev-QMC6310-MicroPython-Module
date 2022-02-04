# Calibrate the sensor by turning it in a circle
# Display the heading

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

magnetometer = PiicoDev_QMC6310()

magnetometer.calibrate()

while True:
    heading = magnetometer.readHeading()
    print(heading)
    sleep_ms(1000)    sleep_ms(100)