_I='calibration.cal'
_H='polar'
_G='z_cal'
_F='y_cal'
_E='x_cal'
_D=None
_C='z'
_B='y'
_A='x'
import math
from PiicoDev_Unified import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=28
_ADDRESS_CR1=10
_ADDRESS_XOUT=1
_ADDRESS_YOUT=3
_ADDRESS_ZOUT=5
class PiicoDev_QMC6310:
	def __init__(self,bus=_D,freq=_D,sda=_D,scl=_D,addr=_I2C_ADDRESS):
		A=0.0;self.x_offset=A;self.y_offset=A;self.z_offset=A
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.i2c.writeto_mem(self.addr,_ADDRESS_CR1,bytes([3]));f=open(_I,'r');f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();self.x_offset=f.readline();f.readline();self.y_offset=f.readline();f.readline();self.z_offset=f.readline();print(self.x_offset);print(self.y_offset);print(self.z_offset)
	def _convertAngleToPositive(self,angle):
		if angle>=360.0:angle=angle-360.0
		if angle<0:angle=angle+360.0
		return angle
	def getControlRegisters(self):return self.i2c.readfrom_mem(self.addr,_ADDRESS_CR1,2)
	def read(self):
		A='little';x=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_XOUT,2),A)
		if x>=32768:x=-(65535-x+1)
		x_cal=x-self.x_offset;y=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_YOUT,2),A)
		if y>=32768:y=-(65535-y+1)
		y_cal=y-self.y_offset;z=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_ZOUT,2),A)
		if z>=32768:z=-(65535-z+1)
		z_cal=z-self.z_offset;return{_A:x,_B:y,_C:z,_E:x_cal,_F:y_cal,_G:z_cal}
	def readPolar(self):cartesian=self.read();pi=math.pi;print(pi);polar=math.atan2(cartesian[_A],cartesian[_B])/pi*180.0;magnitude=math.sqrt(cartesian[_A]*cartesian[_A]+cartesian[_B]*cartesian[_B]+cartesian[_C]*cartesian[_C]);polar=self._convertAngleToPositive(polar);return{_H:polar,'Gauss':magnitude,'mT':magnitude/10.0}
	def readPolarCal(self):cartesian=self.read();pi=math.pi;print(pi);polar=math.atan2(cartesian[_E],cartesian[_F])/pi*180.0;magnitude=math.sqrt(cartesian[_E]*cartesian[_E]+cartesian[_F]*cartesian[_F]+cartesian[_G]*cartesian[_G]);polar=self._convertAngleToPositive(polar);return{_H:polar,'Gauss':magnitude,'mT':magnitude/10.0}
	def readTruePolar(self,declination=float('NaN')):polar=self.readPolar();true_polar=polar[_H]-declination;true_polar=self._convertAngleToPositive(true_polar);return{'true_polar',true_polar}
	def calibrate(self):
		x_min=0;x_max=0;y_min=0;y_max=0;z_min=0;z_max=0
		for i in range(10000):
			cartesian=self.read()
			if cartesian[_A]<x_min:x_min=cartesian[_A]
			if cartesian[_A]>x_max:x_max=cartesian[_A]
			if cartesian[_B]<y_min:y_min=cartesian[_B]
			if cartesian[_B]>y_max:y_max=cartesian[_B]
			if cartesian[_C]<z_min:z_min=cartesian[_C]
			if cartesian[_C]>z_max:z_max=cartesian[_C]
			if i==2000:print('east')
			if i==4000:print('south')
			if i==6000:print('west')
			if i==8000:print('north')
			sleep_ms(1)
		x_offset_new=(x_max+x_min)/2;y_offset_new=(y_max+y_min)/2;z_offset_new=(z_max+z_min)/2;f=open(_I,'w');f.write('x_min:\n'+str(x_min)+'\nx_max:\n'+str(x_max)+'\ny_min:\n'+str(y_min)+'\ny_max:\n'+str(y_max)+'\nz_min\n'+str(z_min)+'\nz_max:\n'+str(z_max)+'\nx_offset:\n');f.write(str(x_offset_new)+'\ny_offset:\n'+str(y_offset_new)+'\nz_offset:\n'+str(z_offset_new));f.close();print('Done')