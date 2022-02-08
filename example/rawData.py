# Prints the raw axis readings in micro-Tesla

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

magSensor = PiicoDev_QMC6310() # Initialise the sensor

while True:
    raw_data = magSensor.read() # Read the field strength on each axis
    print(raw_data)             # Print the data
    sleep_ms(200)
