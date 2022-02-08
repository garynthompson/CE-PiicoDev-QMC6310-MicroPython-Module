# Prints the raw axis readings in micro-Tesla

from PiicoDev_QMC6310 import PiicoDev_QMC6310
from PiicoDev_Unified import sleep_ms

magSensor = PiicoDev_QMC6310()

while True:
    raw_data = magSensor.read()
    print(raw_data)
    sleep_ms(200)
