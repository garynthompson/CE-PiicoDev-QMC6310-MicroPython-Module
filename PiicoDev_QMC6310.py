# https://forum.micropython.org/viewtopic.php?t=3658

import ustruct
from PiicoDev_Unified import *

compat_str = '\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'

_I2C_ADDRESS = 0x1C
_MODE = 0x0A
_XOUT = 0x01
_YOUT = 0x03
_ZOUT = 0x05


class PiicoDev_QMC6310(object):     
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr = _I2C_ADDRESS):
        try:
            if compat_ind >= 1:
                pass
            else:
                print(compat_str)
        except:
            print(compat_str)
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        self.i2c.writeto_mem(self.addr, _MODE, bytes([3]))
    def read(self):
        x = ustruct.unpack(">h",self.i2c.readfrom_mem(self.addr, _XOUT, 2))[0]
        y = ustruct.unpack(">h",self.i2c.readfrom_mem(self.addr, _YOUT, 2))[0]
        z = ustruct.unpack(">h",self.i2c.readfrom_mem(self.addr, _ZOUT, 2))[0]
        return {'x':x,'y':y,'z':z} 
