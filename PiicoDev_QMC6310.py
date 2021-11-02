# https://forum.micropython.org/viewtopic.php?t=3658
# Peter Johnston, Core Electronics

import math
import ustruct
from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_I2C_ADDRESS = 0x1C
_ADDRESS_XOUT = 0x01
_ADDRESS_YOUT = 0x03
_ADDRESS_ZOUT = 0x05
_ADDRESS_STATUS = 0x09
_ADDRESS_CONTROL1 = 0x0A
_ADDRESS_CONTROL2 = 0x0B
_BIT_MODE = 0
_BIT_ODR = 2
_BIT_OSR1 = 4
_BIT_OSR2 = 6
_BIT_RANGE = 2

def _readBit(x, n):
    return x & 1 << n != 0

def _setBit(x, n):
    return x | (1 << n)

def _clearBit(x, n):
    return x & ~(1 << n)

def _writeBit(x, n, b):
    if b == 0:
        return _clearBit(x, n)
    else:
        return _setBit(x, n)

def _writeCrumb(x, n, c):
    x = _writeBit(x, n, _readBit(c, 0))
    return _writeBit(x, n+1, _readBit(c, 1))

class PiicoDev_QMC6310(object):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=_I2C_ADDRESS, odr=0, osr1=0, osr2=3, range=3):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        #self._CR1 = 0xC1 # 11 00 00 01 OSR2 = 8, OSR1 = 8, ODR = 200 Hz, Mode = Normal
        #self._CR2 = 0x0C   # 00 00 11 00 Range = 2 Gauss
        self._CR1 = 0x00
        self._CR2 = 0x00
        self._setMode(1)
        self.setOutputDataRate(odr)
        self.setOverSamplingRatio(osr1)
        self.setOverSamplingRate(osr2)
        self.setRange(range)
        print(self._CR1)
        print(self._CR2)
        #self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))
        #self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL2, bytes([_CR2]))
        self.x_offset = 0
        self.y_offset = 0
        self.z_offset = 0
        try:
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
            self.x_offset = float(f.readline())
            f.readline()
            self.y_offset = float(f.readline())
            f.readline()
            self.z_offset = float(f.readline())
        except:
            print("Calibration is required.  Please run PiicoDev_QMC6310.calibrate().")
            sleep_ms(3000)
        print('X Offset: ' + str(self.x_offset))
        print('Y Offset: ' + str(self.y_offset))
        print('Z Offset: ' + str(self.z_offset))
    
    def _setMode(self, mode):
        self._CR1 = _writeCrumb(self._CR1, _BIT_MODE, mode)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOutputDataRate(self, odr):
        self._CR1 = _writeCrumb(self._CR1, _BIT_ODR, odr)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOverSamplingRatio(self, osr1):
        self._CR1 = _writeCrumb(self._CR1, _BIT_OSR1, osr1)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setOverSamplingRate(self, osr2):
        self._CR1 = _writeCrumb(self._CR1, _BIT_OSR2, osr2)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL1, bytes([self._CR1]))

    def setRange(self, range):
        self._CR2 = _writeCrumb(self._CR2, _BIT_RANGE, range)
        self.i2c.writeto_mem(self.addr, _ADDRESS_CONTROL2, bytes([self._CR2]))

    def _convertAngleToPositive(self, angle):
        if angle >= 360.0:
            angle = angle - 360.0
        if angle < 0:
            angle = angle + 360.0
        return angle
    
    def getControlRegisters(self):
        return self.i2c.readfrom_mem(self.addr, _ADDRESS_CONTROL1, 2)
    
    def _getStatusReady(self, status):
        return _readBit(status, 0)
        
    def _getStatusOverflow(self, status):
        return _readBit(status, 1)
    
    def read(self):
        status = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_STATUS, 1), '')
        if self._getStatusReady(status) is True:
            x = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_XOUT, 2), 'little')
            y = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_YOUT, 2), 'little')
            z = int.from_bytes(self.i2c.readfrom_mem(self.addr, _ADDRESS_ZOUT, 2), 'little')
            if self._getStatusOverflow(status) is True:
                print('Overflow')
                return {'x':float('NaN'),'y':float('NaN'),'z':float('NaN'),'x_cal':float('NaN'),'y_cal':float('NaN'),'z_cal':float('NaN')}
            if (x >= 0x8000):
                x = -((65535 - x) + 1)
            x_cal = x - self.x_offset
            if (y >= 0x8000):
                y = -((65535 - y) + 1)
            y_cal = y - self.y_offset
            if (z >= 0x8000):
                z = -((65535 - z) + 1)
            z_cal = z - self.z_offset
            return {'x':x,'y':y,'z':z,'x_cal':x_cal,'y_cal':y_cal,'z_cal':z_cal}
        else:
            print('Not Ready')
            return {'x':float('NaN'),'y':float('NaN'),'z':float('NaN'),'x_cal':float('NaN'),'y_cal':float('NaN'),'z_cal':float('NaN')}
    
    def readPolar(self):
        cartesian = self.read()
        pi = math.pi
        polar = (math.atan2(cartesian['x'],cartesian['y'])/pi)*180.0
        magnitude = math.sqrt(cartesian['x']*cartesian['x'] + cartesian['y']*cartesian['y'] + cartesian['z']*cartesian['z'])
        polar = self._convertAngleToPositive(polar)
        return {'polar':polar, 'Gauss':magnitude*2/32767, 'uT':magnitude*2/327.67} #mGauss
    
    def readPolarCal(self):
        cartesian = self.read()
        pi = math.pi
        polar = (math.atan2(cartesian['x_cal'],cartesian['y_cal'])/pi)*180.0
        magnitude = math.sqrt(cartesian['x_cal']*cartesian['x_cal'] + cartesian['y_cal']*cartesian['y_cal'] + cartesian['z_cal']*cartesian['z_cal'])
        polar = self._convertAngleToPositive(polar)
        return {'polarCal':polar, 'GaussCal':magnitude*2/32767, 'uTCal':magnitude*2/327.67} #mGauss
    
    def readTruePolar(self, declination=float('NaN')):
        polar = self.readPolarCal()
        true_polar = polar['polarCal'] + declination
        true_polar = self._convertAngleToPositive(true_polar)
        return {'true_polar', true_polar}
    
    def calibrate(self):
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        z_min = 0
        z_max = 0
        log = ''
        print('[          ]', end='')
        range = 3000
        for i in range(range):
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
            if i == range/10:
                print('\015[*         ]', end='')
            if i == 2*range/10:
                print('\015[**        ]', end='')
            if i == 3*range/10:
                print('\015[***       ]', end='')
            if i == 4*range/10:
                print('\015[****      ]', end='')
            if i == 5*range/10:
                print('\015[*****     ]', end='')
            if i == 6*range/10:
                print('\015[******    ]', end='')
            if i == 7*range/10:
                print('\015[*******   ]', end='')
            if i == 8*range/10:
                print('\015[********  ]', end='')
            if i == 9*range/10:
                print('\015[********* ]', end='')
            if i == 10*range/10-1:
                print('\015[**********]')
            log = log + (str(cartesian['x']) + ',' + str(cartesian['y']) + ',' + str(cartesian['z']) + '\n')
            sleep_ms(5)
        x_offset_new = (x_max + x_min) / 2
        y_offset_new = (y_max + y_min) / 2
        z_offset_new = (z_max + z_min) / 2
        f = open("calibration.cal", "w")
        f.write('x_min:\n' + str(x_min) + '\nx_max:\n' + str(x_max) + '\ny_min:\n' + str(y_min) + '\ny_max:\n' + str(y_max) + '\nz_min\n' + str(z_min) + '\nz_max:\n' + str(z_max) + '\nx_offset:\n')
        f.write(str(x_offset_new) + '\ny_offset:\n' + str(y_offset_new) + '\nz_offset:\n' + str(z_offset_new))
        f.close()
        print('x_offset_new: ' + str(x_offset_new))
        print('y_offset_new: ' + str(y_offset_new))
        print('z_offset_new: ' + str(z_offset_new))
        flog = open("calibration.log", "w")
        flog.write(log)
        flog.close
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