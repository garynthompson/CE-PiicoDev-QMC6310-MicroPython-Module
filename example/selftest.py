# Calibrate the sensor by turning it in a circle
# Display the heading with compensation for magnetic declination

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms          # Cross-platform compatible sleep function

sensor = PiicoDev_QMC6310(range=200)          # Initialise the sensor with 800uT range. Valid ranges: 200, 800, 1200, 3000 uT
sleep_ms(5)
while True:
    sensor.selfTest()
    sleep_ms(200)
