_J='polarCal'
_I='calibration.cal'
_H=None
_G='z_cal'
_F='y_cal'
_E='x_cal'
_D='z'
_C='y'
_B='x'
_A='NaN'
import math,ustruct
from PiicoDev_Unified import *
compat_str='\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n'
_I2C_ADDRESS=28
_ADDRESS_XOUT=1
_ADDRESS_YOUT=3
_ADDRESS_ZOUT=5
_ADDRESS_Status=9
_ADDRESS_Control1=10
_ADDRESS_Control2=11
class PiicoDev_QMC6310:
	def __init__(self,bus=_H,freq=_H,sda=_H,scl=_H,addr=_I2C_ADDRESS):
		try:
			if compat_ind>=1:0
			else:print(compat_str)
		except:print(compat_str)
		self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;_CR1=205;_CR2=12;self.i2c.writeto_mem(self.addr,_ADDRESS_Control1,bytes([_CR1]));self.i2c.writeto_mem(self.addr,_ADDRESS_Control2,bytes([_CR2]));self.x_offset=0;self.y_offset=0;self.z_offset=0
		try:f=open(_I,'r');f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();f.readline();self.x_offset=float(f.readline());f.readline();self.y_offset=float(f.readline());f.readline();self.z_offset=float(f.readline())
		except:print('Calibration is required.  Please run PiicoDev_QMC6310.calibrate().')
		print('X Offset: '+str(self.x_offset));print('Y Offset: '+str(self.y_offset));print('Z Offset: '+str(self.z_offset))
	def _convertAngleToPositive(self,angle):
		if angle>=360.0:angle=angle-360.0
		if angle<0:angle=angle+360.0
		return angle
	def getControlRegisters(self):return self.i2c.readfrom_mem(self.addr,_ADDRESS_Control1,2)
	def _getStatusReady(self,status):return status&1<<0!=0
	def _getStatusOverflow(self,status):return status&1<<1!=0
	def read(self):
		A='little';status=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_Status,1),'')
		if self._getStatusReady(status)is True:
			x=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_XOUT,2),A);y=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_YOUT,2),A);z=int.from_bytes(self.i2c.readfrom_mem(self.addr,_ADDRESS_ZOUT,2),A)
			if self._getStatusOverflow(status)is True:print('Overflow');return{_B:float(_A),_C:float(_A),_D:float(_A),_E:float(_A),_F:float(_A),_G:float(_A)}
			if x>=32768:x=-(65535-x+1)
			x_cal=x-self.x_offset
			if y>=32768:y=-(65535-y+1)
			y_cal=y-self.y_offset
			if z>=32768:z=-(65535-z+1)
			z_cal=z-self.z_offset;return{_B:x,_C:y,_D:z,_E:x_cal,_F:y_cal,_G:z_cal}
		else:print('Not Ready');return{_B:float(_A),_C:float(_A),_D:float(_A),_E:float(_A),_F:float(_A),_G:float(_A)}
	def readPolar(self):cartesian=self.read();pi=math.pi;polar=math.atan2(cartesian[_B],cartesian[_C])/pi*180.0;magnitude=math.sqrt(cartesian[_B]*cartesian[_B]+cartesian[_C]*cartesian[_C]+cartesian[_D]*cartesian[_D]);polar=self._convertAngleToPositive(polar);return{'polar':polar,'Gauss':magnitude*2/32767,'uT':magnitude*2/327.67}
	def readPolarCal(self):cartesian=self.read();pi=math.pi;polar=math.atan2(cartesian[_E],cartesian[_F])/pi*180.0;magnitude=math.sqrt(cartesian[_E]*cartesian[_E]+cartesian[_F]*cartesian[_F]+cartesian[_G]*cartesian[_G]);polar=self._convertAngleToPositive(polar);return{_J:polar,'GaussCal':magnitude*2/32767,'uTCal':magnitude*2/327.67}
	def readTruePolar(self,declination=float(_A)):polar=self.readPolarCal();true_polar=polar[_J]+declination;true_polar=self._convertAngleToPositive(true_polar);return{'true_polar',true_polar}
	def calibrate(self):
		x_min=0;x_max=0;y_min=0;y_max=0;z_min=0;z_max=0;log='';print('[          ]',end='');range=3000
		for i in range(range):
			cartesian=self.read()
			if cartesian[_B]<x_min:x_min=cartesian[_B]
			if cartesian[_B]>x_max:x_max=cartesian[_B]
			if cartesian[_C]<y_min:y_min=cartesian[_C]
			if cartesian[_C]>y_max:y_max=cartesian[_C]
			if cartesian[_D]<z_min:z_min=cartesian[_D]
			if cartesian[_D]>z_max:z_max=cartesian[_D]
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
			log=log+(str(cartesian[_B])+','+str(cartesian[_C])+','+str(cartesian[_D])+'\n');sleep_ms(5)
		x_offset_new=(x_max+x_min)/2;y_offset_new=(y_max+y_min)/2;z_offset_new=(z_max+z_min)/2;f=open(_I,'w');f.write('x_min:\n'+str(x_min)+'\nx_max:\n'+str(x_max)+'\ny_min:\n'+str(y_min)+'\ny_max:\n'+str(y_max)+'\nz_min\n'+str(z_min)+'\nz_max:\n'+str(z_max)+'\nx_offset:\n');f.write(str(x_offset_new)+'\ny_offset:\n'+str(y_offset_new)+'\nz_offset:\n'+str(z_offset_new));f.close();print('x_offset_new: '+str(x_offset_new));print('y_offset_new: '+str(y_offset_new));print('z_offset_new: '+str(z_offset_new));flog=open('calibration.log','w');flog.write(log);flog.close