_L='polar_true'
_K='polar_cal'
_J='Gauss_cal'
_I='uT_cal'
_H='z_cal'
_G=None
_F='y_cal'
_E='x_cal'
_D='NaN'
_C='z'
_B='y'
_A='x'
import math,ustruct
from PiicoDev_Unified import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=28
_ADDRESS_XOUT=1
_ADDRESS_YOUT=3
_ADDRESS_ZOUT=5
_ADDRESS_STATUS=9
_ADDRESS_CONTROL1=10
_ADDRESS_CONTROL2=11
_BIT_MODE=0
_BIT_ODR=2
_BIT_OSR1=4
_BIT_OSR2=6
_BIT_RANGE=2
def _readBit(x,n):return x&1<<n!=0
def _setBit(x,n):return x|1<<n
def _clearBit(x,n):return x&~(1<<n)
def _writeBit(x,n,b):
	if b==0:return _clearBit(x,n)
	else:return _setBit(x,n)
def _writeCrumb(x,n,c):x=_writeBit(x,n,_readBit(c,0));return _writeBit(x,n+1,_readBit(c,1))
class PiicoDev_QMC6310:
	def __init__(self,bus=_G,freq=_G,sda=_G,scl=_G,addr=_I2C_ADDRESS,odr=0,osr1=0,osr2=3,range=3,cal_filename='calibration.cal'):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.odr=odr;self.cal_filename=cal_filename;self._CR1=0;self._CR2=0
		try:self._setMode(1);self.setOutputDataRate(odr);self.setOverSamplingRatio(osr1);self.setOverSamplingRate(osr2);self.setRange(range)
		except Exception as e:print(i2c_err_str.format(self.addr));raise e
		self.x_offset=0;self.y_offset=0;self.z_offset=0;self.loadCalibration()
	def _setMode(self,mode):self._CR1=_writeCrumb(self._CR1,_BIT_MODE,mode);self.i2c.writeto_mem(self.addr,_ADDRESS_CONTROL1,bytes([self._CR1]))
	def setOutputDataRate(self,odr):self._CR1=_writeCrumb(self._CR1,_BIT_ODR,odr);self.i2c.writeto_mem(self.addr,_ADDRESS_CONTROL1,bytes([self._CR1]))
	def setOverSamplingRatio(self,osr1):self._CR1=_writeCrumb(self._CR1,_BIT_OSR1,osr1);self.i2c.writeto_mem(self.addr,_ADDRESS_CONTROL1,bytes([self._CR1]))
	def setOverSamplingRate(self,osr2):self._CR1=_writeCrumb(self._CR1,_BIT_OSR2,osr2);self.i2c.writeto_mem(self.addr,_ADDRESS_CONTROL1,bytes([self._CR1]))
	def setRange(self,range):self._CR2=_writeCrumb(self._CR2,_BIT_RANGE,range);self.i2c.writeto_mem(self.addr,_ADDRESS_CONTROL2,bytes([self._CR2]))
	def _convertAngleToPositive(self,angle):
		if angle>=360.0:angle=angle-360.0
		if angle<0:angle=angle+360.0
		return angle
	def _getControlRegisters(self):return self.i2c.readfrom_mem(self.addr,_ADDRESS_CONTROL1,2)
	def _getStatusReady(self,status):return _readBit(status,0)
	def _getStatusOverflow(self,status):return _readBit(status,1)
	def read(self):
		A='little';NaN={_A:float(_D),_B:float(_D),_C:float(_D),_E:float(_D),_F:float(_D),_H:float(_D)}
		try:status=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_STATUS,1),'')
		except:print(i2c_err_str.format(self.addr));return NaN
		if self._getStatusReady(status)is True:
			try:x=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_XOUT,2),A);y=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_YOUT,2),A);z=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_ZOUT,2),A)
			except:print(i2c_err_str.format(self.addr));return NaN
			if self._getStatusOverflow(status)is True:print('Overflow');return NaN
			if x>=32768:x=-(65535-x+1)
			x_cal=x-self.x_offset
			if y>=32768:y=-(65535-y+1)
			y_cal=y-self.y_offset
			if z>=32768:z=-(65535-z+1)
			z_cal=z-self.z_offset;return{_A:x,_B:y,_C:z,_E:x_cal,_F:y_cal,_H:z_cal}
		else:print('Not Ready');return NaN
	def readPolar(self):cartesian=self.read();pi=math.pi;polar=math.atan2(cartesian[_A],cartesian[_B])/pi*180.0;magnitude=math.sqrt(cartesian[_A]*cartesian[_A]+cartesian[_B]*cartesian[_B]+cartesian[_C]*cartesian[_C]);polar=self._convertAngleToPositive(polar);return{'polar':polar,'Gauss':magnitude*2/32767,'uT':magnitude*2/327.67}
	def readPolarCal(self):cartesian=self.read();pi=math.pi;polar=math.atan2(cartesian[_E],cartesian[_F])/pi*180.0;magnitude=math.sqrt(cartesian[_E]*cartesian[_E]+cartesian[_F]*cartesian[_F]+cartesian[_H]*cartesian[_H]);polar=self._convertAngleToPositive(polar);return{_K:polar,_J:magnitude*2/32767,_I:magnitude*2/327.67}
	def readTruePolar(self,declination=float(_D)):polar=self.readPolarCal();polar_true=polar[_K]+declination;polar_true=self._convertAngleToPositive(polar_true);return{_L:polar_true,_J:polar[_J],_I:polar[_I]}
	def readMagnitude(self):return self.readTruePolar()[_I]
	def readHeading(self,declination=0):return self.readTruePolar(declination=declination)[_L]
	def calibrate(self,enable_logging=False):
		try:self.setOutputDataRate(3)
		except Exception as e:print(i2c_err_str.format(self.addr));raise e
		x_min=0;x_max=0;y_min=0;y_max=0;z_min=0;z_max=0;log='';print('If calibrating for X & Y eg the QMC6310 is to be used as a compass, rotate the QMC6310 on a flat surface and keep the unit flat at all times until the bar below is completely populated with stars.  If the QMC6310 is to be used as a three-dimentional magnetometer, rotate in all three dimentions until the bar below is completely populated with stars.');print('[          ]',end='');range=1000;i=0
		while i<range:
			i+=1;sleep_ms(5);cartesian=self.read()
			if cartesian[_A]<x_min:x_min=cartesian[_A];i=0
			if cartesian[_A]>x_max:x_max=cartesian[_A];i=0
			if cartesian[_B]<y_min:y_min=cartesian[_B];i=0
			if cartesian[_B]>y_max:y_max=cartesian[_B];i=0
			if cartesian[_C]<z_min:z_min=cartesian[_C];i=0
			if cartesian[_C]>z_max:z_max=cartesian[_C];i=0
			if i==range/10:print('\r[*         ]',end='')
			if i==2*range/10:print('\r[**        ]',end='')
			if i==3*range/10:print('\r[***       ]',end='')
			if i==4*range/10:print('\r[****      ]',end='')
			if i==5*range/10:print('\r[*****     ]',end='')
			if i==6*range/10:print('\r[******    ]',end='')
			if i==7*range/10:print('\r[*******   ]',end='')
			if i==8*range/10:print('\r[********  ]',end='')
			if i==9*range/10:print('\r[********* ]',end='')
			if i==10*range/10-1:print('\r[**********]')
			if enable_logging:log=log+(str(cartesian[_A])+','+str(cartesian[_B])+','+str(cartesian[_C])+'\n')
		self.setOutputDataRate(self.odr);x_offset_new=(x_max+x_min)/2;y_offset_new=(y_max+y_min)/2;z_offset_new=(z_max+z_min)/2;f=open(self.cal_filename,'w');f.write('x_min:\n'+str(x_min)+'\nx_max:\n'+str(x_max)+'\ny_min:\n'+str(y_min)+'\ny_max:\n'+str(y_max)+'\nz_min\n'+str(z_min)+'\nz_max:\n'+str(z_max)+'\nx_offset:\n');f.write(str(x_offset_new)+'\ny_offset:\n'+str(y_offset_new)+'\nz_offset:\n'+str(z_offset_new));f.close()
		if enable_logging:flog=open('calibration.log','w');flog.write(log);flog.close
		self.loadCalibration()
	def loadCalibration(self):
		try:f=open(self.cal_filename,'r');f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();self.x_offset=float(f.readline());f.readline();self.y_offset=float(f.readline());f.readline();self.z_offset=float(f.readline())
		except:print('Calibration is required.  Please run calibrate().  Visit piico.dev/p15 for more info.');sleep_ms(3000)
		print('X Offset: '+str(self.x_offset));print('Y Offset: '+str(self.y_offset));print('Z Offset: '+str(self.z_offset))