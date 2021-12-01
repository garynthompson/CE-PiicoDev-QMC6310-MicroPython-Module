# strong magnet detector
from PiicoDev_QMC6310 import *

magnetometer = PiicoDev_QMC6310()

while True:
    magnet_detected = False
    threshold = 50 # uT
    magnitude = magnetometer.readMagnitude()
    if magnitude <= threshold:
        magnet_detected = False
    if magnitude > threshold:
        magnet_detected = True
    if magnet_detected is True:
        print('Strong magnet detected nearby.', end='')
    else:
        print('No strong magnet detected.', end='')
    print(' Magnetic field strength: ', end='')
    print(magnitude, end='')
    print(' uT')
    sleep_ms(1000)