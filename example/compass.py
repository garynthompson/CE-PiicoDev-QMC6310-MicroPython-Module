# Calibrate the sensor by turning it in a circle
# Display the heading with compensation for magnetic declination

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

compass = PiicoDev_QMC6310(range=200) # Initialise the sensor with the most sensitive range. Valid ranges: 200, 800, 1200, 3000 uT

compass.calibrate() # only need to calibrate once

# Declination is the difference between magnetic-north and true-north ("heading") and depends on location
compass.setDeclination(12.5) # Found with: https://www.magnetic-declination.com/Australia/Newcastle/122944.html

while True:
    heading = compass.readHeading()
    print(heading)
    sleep_ms(100)