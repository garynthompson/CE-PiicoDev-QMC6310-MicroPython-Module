# calibrated data
from PiicoDev_QMC6310 import *

magnetometer = PiicoDev_QMC6310()

while True:
    cal_data = magnetometer.read()
    print('X: ', end='')
    print(cal_data['x_cal'],end='')
    print('   Y: ', end='')
    print(cal_data['y_cal'],end='')
    print('   Z: ', end='')
    print(cal_data['z_cal'])
    
    sleep_ms(1000)