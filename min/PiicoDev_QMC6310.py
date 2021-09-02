_A=None
import ustruct
from PiicoDev_Unified import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=28
_MODE=10
_XOUT=1
_YOUT=3
_ZOUT=5
class PiicoDev_QMC6310:
	def __init__(self,bus=_A,freq=_A,sda=_A,scl=_A,addr=_I2C_ADDRESS):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.i2c.writeto_mem(self.addr,_MODE,bytes([3]))
	def read(self):A='>h';x=ustruct.unpack(A,self.i2c.readfrom_mem(self.addr,_XOUT,2))[0];y=ustruct.unpack(A,self.i2c.readfrom_mem(self.addr,_YOUT,2))[0];z=ustruct.unpack(A,self.i2c.readfrom_mem(self.addr,_ZOUT,2))[0];return{'x':x,'y':y,'z':z}