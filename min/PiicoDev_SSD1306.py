_F='big'
_E='Linux'
_D='microbit'
_C=b'@'
_B=False
_A=None
from PiicoDev_Unified import *
_SYSNAME=os.uname().sysname
zoom=1
if _SYSNAME==_D:from microbit import *;from utime import sleep_ms
elif _SYSNAME==_E:from PIL import Image,ImageDraw,ImageFont
else:import framebuf
_SET_CONTRAST=129
_SET_ENTIRE_ON=164
_SET_NORM_INV=166
_SET_DISP=174
_SET_MEM_ADDR=32
_SET_COL_ADDR=33
_SET_PAGE_ADDR=34
_SET_DISP_START_LINE=64
_SET_SEG_REMAP=160
_SET_MUX_RATIO=168
_SET_COM_OUT_DIR=192
_SET_DISP_OFFSET=211
_SET_COM_PIN_CFG=218
_SET_DISP_CLK_DIV=213
_SET_PRECHARGE=217
_SET_VCOM_DESEL=219
_SET_CHARGE_PUMP=141
class PiicoDev_SSD1306:
	def init_display(self):
		for cmd in (_SET_DISP,_SET_MEM_ADDR,0,_SET_DISP_START_LINE,_SET_SEG_REMAP|1,_SET_MUX_RATIO,self.height-1,_SET_COM_OUT_DIR|8,_SET_DISP_OFFSET,0,_SET_COM_PIN_CFG,2 if self.width>2*self.height else 18,_SET_DISP_CLK_DIV,128,_SET_PRECHARGE,34 if self.external_vcc else 241,_SET_VCOM_DESEL,48,_SET_CONTRAST,255,_SET_ENTIRE_ON,_SET_NORM_INV,_SET_CHARGE_PUMP,16 if self.external_vcc else 20,_SET_DISP|1):print(cmd);self.write_cmd(cmd)
		self.fill(0);self.show()
	def poweroff(self):self.write_cmd(_SET_DISP)
	def poweron(self):self.write_cmd(_SET_DISP|1)
	def setContrast(self,contrast):self.write_cmd(_SET_CONTRAST);self.write_cmd(contrast)
	def invert(self,invert):self.write_cmd(_SET_NORM_INV|invert&1)
	def rotate(self,rotate):self.write_cmd(_SET_COM_OUT_DIR|(rotate&1)<<3);self.write_cmd(_SET_SEG_REMAP|rotate&1)
	def show(self):
		print('showing display');x0=0;x1=self.width-1
		if self.width==64:x0+=32;x1+=32
		self.write_cmd(_SET_COL_ADDR);self.write_cmd(x0);self.write_cmd(x1);self.write_cmd(_SET_PAGE_ADDR);self.write_cmd(0);self.write_cmd(self.pages-1);self.write_data(self.buffer)
	def write_cmd(self,cmd):self.i2c.writeto_mem(self.addr,int.from_bytes(b'\x80',_F),bytes([cmd]))
	def write_data(self,buf):self.write_list[1]=buf;self.i2c.writeto_mem(self.addr,int.from_bytes(self.write_list[0],_F),self.write_list[1])
	def set_pos(self,col=0,page=0):self.write_cmd(176|page);c1,c2=col*2&15,col>>3;self.write_cmd(0|c1);self.write_cmd(16|c2)
	def set_zoom(self,v):global zoom;self.write_cmd(214+v);self.write_cmd(167-v);zoom=v
	def draw_screen(self):self.set_zoom(1);self.set_pos();self.write_data(self.buffer)
class PiicoDev_SSD1306_MicroPython(PiicoDev_SSD1306):
	def __init__(self,width,height,bus=_A,freq=_A,sda=_A,scl=_A,addr=60,external_vcc=_B):self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.temp=bytearray(2);self.write_list=[_C,_A];self.width=width;self.height=height;self.external_vcc=external_vcc;self.pages=self.height//8;self.buffer=bytearray(self.pages*self.width);print('Setting up on RaspberryPi Pico');self.fbuf=framebuf.FrameBuffer(self.buffer,width,height,framebuf.MONO_VLSB);self.fill=self.fbuf.fill;self.hline=self.fbuf.hline;self.text=self.fbuf.text;self.fill_rect=self.fbuf.fill_rect;self.init_display()
class PiicoDev_SSD1306_MicroBit(PiicoDev_SSD1306):
	def __init__(self,width,height,bus=_A,freq=_A,sda=_A,scl=_A,addr=60,external_vcc=_B):self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.temp=bytearray(2);self.write_list=[_C,_A];self.width=width;self.height=height;self.external_vcc=external_vcc;self.pages=self.height//8;self.buffer=bytearray(self.pages*self.width);self.text=self.text;self.fill=self.fill;self.init_display()
	def fill(self,c=0):
		global screen;self.set_pos()
		for i in range(1,513):self.buffer[i]=c
		self.draw_screen()
	def text(self,text,x,y,colour):
		x=int(x/15);y=int(y/15)
		for i in range(0,min(len(text),12-x)):
			for c in range(0,5):
				col=0
				for r in range(1,6):p=Image(text[i]).get_pixel(c,r-1);col=col|1<<r if p!=0 else col
				ind=x*10+y*128+i*10+c*2+1;self.buffer[ind],self.buffer[ind+1]=col,col
		if colour>0:self.set_zoom(1);self.set_pos(x*10,y*2);ind0=x*10+y*128+1;self.write_data(self.buffer[ind0:ind+1])
class PiicoDev_SSD1306_Linux(PiicoDev_SSD1306):
	def __init__(self,width,height,bus=_A,freq=_A,sda=_A,scl=_A,addr=60,external_vcc=_B):self.i2c=create_unified_i2c(bus=bus,freq=freq,sda=sda,scl=scl);self.addr=addr;self.temp=bytearray(2);self.write_list=[_C,_A];self.width=width;self.height=height;self.external_vcc=external_vcc;self.pages=self.height//8;self.buffer=bytearray(self.pages*self.width);self.image=Image.new('1',(width,height));self.draw=ImageDraw.Draw(self.image);self.text=self.text;self.fill=self.fill;self.hline=self.hline;self.font=ImageFont.load_default();self.fill=self.fill;self.init_display()
	def fill(self,c=0):
		global screen;self.set_pos()
		for i in range(1,513):self.buffer[i]=c
		self.draw_screen()
	def text(self,text,x,y,colour):print('Running Text Python');self.draw.text((x,y),text,fill=255,font=self.font)
	def fill_rect(self,x,y,width,height,colour):self.draw.rectangle((x,y,width+x,height+y),fill=colour)
	def hline(self,x,y,width,colour):self.draw.line([(x,y),(x+width,y)],width=1,fill=colour)
	def imagesend(self,image):
		'Set buffer to value of Python Imaging Library image.  The image should\n        be in 1 bit mode and a size equal to the display size.\n        '
		if image.mode!='1':raise ValueError('Image must be in mode 1.')
		imwidth,imheight=image.size
		if imwidth!=self.width or imheight!=self.height:raise ValueError('Image must be same dimensions as display ({0}x{1}).'.format(self.width,self.height))
		pix=image.load();index=0
		for page in range(self.pages):
			for x in range(self.width):
				bits=0
				for bit in [0,1,2,3,4,5,6,7]:bits=bits<<1;bits|=0 if pix[x,page*8+7-bit]==0 else 1
				self.buffer[index]=bits;index+=1
def create_PiicoDev_SSD1306(width,height,addr=_A,bus=_A,freq=_A,sda=_A,scl=_A):
	if _SYSNAME==_D:display=PiicoDev_SSD1306_MicroBit(width=width,height=height,addr=addr,freq=freq)
	elif _SYSNAME==_E:display=PiicoDev_SSD1306_Linux(width=width,height=height,addr=addr,freq=freq)
	else:display=PiicoDev_SSD1306_MicroPython(width=width,height=height,addr=addr,bus=bus,freq=freq,sda=sda,scl=scl)
	return display