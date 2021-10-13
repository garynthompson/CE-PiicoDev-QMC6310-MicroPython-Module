# https://forum.micropython.org/viewtopic.php?t=3658

import math
from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_I2C_ADDRESS = 0x1C
_ADDRESS_CR1 = 0x0A
_ADDRESS_XOUT = 0x01
_ADDRESS_YOUT = 0x03
_ADDRESS_ZOUT = 0x05

class PiicoDev_QMC6310(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr = _I2C_ADDRESS):
        self.x_offset = 0.0
        self.y_offset = 0.0
        self.z_offset = 0.0
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        self.i2c.writeto_mem(self.addr, _ADDRESS_CR1, bytes([3]))
        f = open("calibration.cal", "r")
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        f.readline()
        self.x_offset = f.readline()
        f.readline()
        self.y_offset = f.readline()
        f.readline()
        self.z_offset = f.readline()
        print(self.x_offset)
        print(self.y_offset)
        print(self.z_offset)
    
    def _convertAngleToPositive(self, angle):
        if angle >= 360.0:
            angle = angle - 360.0
        if angle < 0:
            angle = angle + 360.0
        return angle
    
    def getControlRegisters(self):
        return self.i2c.readfrom_mem(self.addr, _ADDRESS_CR1, 2)
    
    def read(self):
        x = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_XOUT, 2), 'little')
        if (x >= 0x8000):
            x = -((65535 - x) + 1)
        x_cal = x - self.x_offset
        y = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_YOUT, 2), 'little')
        if (y >= 0x8000):
            y = -((65535 - y) + 1)
        y_cal = y - self.y_offset
        z = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_ZOUT, 2), 'little')
        if (z >= 0x8000):
            z = -((65535 - z) + 1)
        z_cal = z - self.z_offset
        return {'x':x,'y':y,'z':z,'x_cal':x_cal,'y_cal':y_cal,'z_cal':z_cal}
    
    def readPolar(self):
        cartesian = self.read()
        pi = math.pi
        print(pi)
        polar = (math.atan2(cartesian['x'],cartesian['y'])/pi)*180.0
        magnitude = math.sqrt(cartesian['x']*cartesian['x'] + cartesian['y']*cartesian['y'] + cartesian['z']*cartesian['z'])
        polar = self._convertAngleToPositive(polar)
        return {'polar':polar, 'Gauss':magnitude, 'mT':magnitude/10.0} #mGauss
    
    def readPolarCal(self):
        cartesian = self.read()
        pi = math.pi
        print(pi)
        polar = (math.atan2(cartesian['x_cal'],cartesian['y_cal'])/pi)*180.0
        magnitude = math.sqrt(cartesian['x_cal']*cartesian['x_cal'] + cartesian['y_cal']*cartesian['y_cal'] + cartesian['z_cal']*cartesian['z_cal'])
        polar = self._convertAngleToPositive(polar)
        return {'polar':polar, 'Gauss':magnitude, 'mT':magnitude/10.0} #mGauss
    
    def readTruePolar(self, declination=float('NaN')):
        polar = self.readPolar()
        true_polar = polar['polar'] - declination
        true_polar = self._convertAngleToPositive(true_polar)
        return {'true_polar', true_polar}
    
    def calibrate(self):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        z_min = 0
        z_max = 0
        for i in range(10000):
            cartesian = self.read()
#             print(cartesian)
            if cartesian['x'] < x_min:
                x_min = cartesian['x']
            if cartesian['x'] > x_max:
                x_max = cartesian['x']
            if cartesian['y'] < y_min:
                y_min = cartesian['y']
            if cartesian['y'] > y_max:
                y_max = cartesian['y']
            if cartesian['z'] < z_min:
                z_min = cartesian['z']
            if cartesian['z'] > z_max:
                z_max = cartesian['z']
            if i == 2000:
                print('east')
            if i == 4000:
                print('south')
            if i == 6000:
                print('west')
            if i == 8000:
                print('north')
            sleep_ms(1)
        x_offset_new = (x_max + x_min) / 2
        y_offset_new = (y_max + y_min) / 2
        z_offset_new = (z_max + z_min) / 2
        f = open("calibration.cal", "w")
        f.write('x_min:\n' + str(x_min) + '\nx_max:\n' + str(x_max) + '\ny_min:\n' + str(y_min) + '\ny_max:\n' + str(y_max) + '\nz_min\n' + str(z_min) + '\nz_max:\n' + str(z_max) + '\nx_offset:\n')
        f.write(str(x_offset_new) + '\ny_offset:\n' + str(y_offset_new) + '\nz_offset:\n' + str(z_offset_new))
        f.close()
        print('Done')
               
#             print('x_min' + str(x_min))
#             print('x_max' + str(x_max))
#             print('y_min' + str(y_min))
#             print('y_max' + str(y_max))
#             print('z_min' + str(z_min))
#             print('z_max' + str(z_max))
#     def readInclination(self):
#         cartesian = self.read()
#         pi = math.pi
#         print(pi)
#         polar = (math.atan2(math.sqrt(cartesian['x']*cartesian['x']+cartesian['y']*cartesian['y']),cartesian['z'])/pi)*180.0
#         magnitude = math.sqrt(cartesian['x']*cartesian['x'] + cartesian['y']*cartesian['y'] + cartesian['z']*cartesian['z'])
#         polar = self._convertAngleToPositive(polar)
#         return {'inclination':polar}

#todo returnfloat('NaN') when disconnected