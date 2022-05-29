from micropython import const
from machine import Pin
from utime import sleep_ms, sleep_us

                                                                                   
TM1637_DELAY_US = const(4)

TM1637_BRIGHTNESS_MIN = const(0x00)
TM1637_BRIGHTNESS_1 = const(0x01)
TM1637_BRIGHTNESS_2 = const(0x02)
TM1637_BRIGHTNESS_3 = const(0x03)
TM1637_BRIGHTNESS_4 = const(0x04)
TM1637_BRIGHTNESS_5 = const(0x05)                                           
TM1637_BRIGHTNESS_6 = const(0x06)
TM1637_BRIGHTNESS_MAX = const(0x07)
                                                             
TM1637_POSITION_MAX = const(0x06)

TM1637_CMD_SET_DATA = const(0x40)
TM1637_CMD_SET_ADDR = const(0xC0)
TM1637_CMD_SET_DISPLAY = const(0x80)                           

TM1637_SET_DATA_WRITE = const(0x00)
TM1637_SET_DATA_READ = const(0x02)
TM1637_SET_DATA_A_ADDR = const(0x00)
TM1637_SET_DATA_F_ADDR = const(0x04)
TM1637_SET_DATA_M_NORM = const(0x00)
TM1637_SET_DATA_M_TEST = const(0x10)
TM1637_SET_DISPLAY_OFF = const( 0x00)    
TM1637_SET_DISPLAY_ON = const(0x08)


seg_code_list = [
  0x00, # (32) 	<space>
  0x86, # (33)		!
  0x22, # (34)		"      
  0x7E, # (35)		#  
  0x6D, # (36)		$
  0x00, # (37)		%
  0x00, # (38)		&   
  0x02, # (39)		'
  0x30, # (40)		(
  0x06, # (41)		)                         
  0x63, # (42)		*
  0x00, # (43)		+
  0x04, # (44)		,                                                   
  0x40, # (45)		-
  0x80, # (46)		.                                   
  0x52, # (47)		/
  0x3F, # (48)		0
  0x06, # (49)		1
  0x5B, # (50)		2
  0x4F, # (51)		3
  0x66, # (52)		4  
  0x6D, # (53)		5  
  0x7D, # (54)		6  
  0x27, # (55)		7
  0x7F, # (56)		8  
  0x6F, # (57)		9  
  0x00, # (58)		:
  0x00, # (59)		;  
  0x00, # (60)		<  
  0x48, # (61)		=
  0x00, # (62)		>  
  0x53, # (63)		?
  0x5E, # (64)		@  
  0x77, # (65)		A  
  0x7E, # (66)		B  
  0x39, # (67)		C  
  0x3E, # (68)		D  
  0x79, # (69)		E  
  0x71, # (70)		F  
  0x3D, # (71)		G  
  0x76, # (72)		H  
  0x06, # (73)		I  
  0x1F, # (74)		J
  0x69, # (75)		K
  0x38, # (76)		L
  0x15, # (77)		M
  0x37, # (78)		N
  0x3F, # (79)		O
  0x73, # (80)		P
  0x67, # (81)		Q
  0x31, # (82)		R  
  0x6D, # (83)		S
  0x78, # (84)		T
  0x3E, # (85)		U
  0x2A, # (86)		V
  0x1D, # (87)		W
  0x76, # (88)		X
  0x6E, # (89)		Y
  0x5B, # (90)		Z
  0x39, # (91)		[
  0x64, # (92)		\ 
  0x0F, # (93)		]
  0x00, # (94)		^
  0x08, # (95)		_
  0x20, # (96)		`
  0x5F, # (97)		a                                                      
  0x7C, # (98)		b
  0x58, # (99)		c
  0x5E, # (100)	d
  0x7B, # (101)	e
  0x31, # (102)	f
  0x6F, # (103)	g
  0x74, # (104)	h
  0x04, # (105)	i
  0x0E, # (106)	j
  0x75, # (107)	k
  0x30, # (108)	l
  0x55, # (109)	m
  0x54, # (110)	n
  0x5C, # (111)	o
  0x73, # (112)	p
  0x67, # (113)	q
  0x50, # (114)	r
  0x6D, # (115)	s
  0x78, # (116)	t
  0x1C, # (117)	u
  0x2A, # (118)	v
  0x1D, # (119)	w
  0x76, # (120)	x
  0x6E, # (121)	y
  0x47, # (122)	z        
  0x46, # (123)	{
  0x06, # (124)	|
  0x70, # (125)	}
  0x01  # (126)	~
]


seg_pos_list = [
    0x02, # 1st
    0x01, # 2nd
    0x00, # 3rd
    0x05, # 4th
    0x04, # 5th
    0x03, # 6th  
]


class TM1637():
    def __init__(self, _dat_pin, _clk_pin, no_of_displays = TM1637_POSITION_MAX):
        self.dat_pin = Pin(_dat_pin, Pin.OUT)
        self.clk_pin = Pin(_clk_pin, Pin.OUT)
        self.seg_max_cnt = no_of_displays
        
        self.init()
        
        
    def init(self):
        self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
        
        self.dat_pin.off()
        self.clk_pin.off()
        
        self.send_command(TM1637_CMD_SET_DISPLAY | TM1637_BRIGHTNESS_4 | TM1637_SET_DISPLAY_ON)
        self.clear()
        
        
    def start(self):
        self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
        
        self.dat_pin.on()
        self.clk_pin.on()
        sleep_us(TM1637_DELAY_US)
        self.dat_pin.off()
        
        
    def stop(self):
        self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
        
        self.clk_pin.off()
        sleep_us(TM1637_DELAY_US)
        self.dat_pin.off()
        sleep_us(TM1637_DELAY_US)
        self.clk_pin.on()
        sleep_us(TM1637_DELAY_US)
        self.dat_pin.on()
        
    
    def write(self, value):
        self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
        
        i = 0
        ack = 0
        
        for i in range (0, 8):
            self.clk_pin.off()
            sleep_us(TM1637_DELAY_US)
            self.dat_pin(value & 0x01)
            self.clk_pin.on()
            sleep_us(TM1637_DELAY_US)
            value >>= 1
            
        self.clk_pin.off()
        sleep_us(TM1637_DELAY_US)
        
        self.dat_pin.init(Pin.IN, Pin.PULL_UP)

        ack = self.dat_pin.value()
        
        if(ack != 0):
            self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
            self.dat_pin.off()
            
        self.dat_pin.init(Pin.OUT, Pin.PULL_DOWN)
        sleep_us(TM1637_DELAY_US)
        
        self.clk_pin.on()
        sleep_us(TM1637_DELAY_US)
        self.clk_pin.off()
        sleep_us(TM1637_DELAY_US)
        
        return ack
    
    
    def send_command(self, value):
        self.start()
        self.write(value)
        self.stop()
        
    
    def clear(self):
        for i in range(0, self.seg_max_cnt):
            self.display(i , ' ', 0x00)
            
            
    def display(self, pos, seg_code, dot_state):
        temp = 0
    
        temp = seg_code_list[((ord(seg_code)) - 0x20)]
        
        if(dot_state == 1):
            temp |= seg_code_list[14]
        
        self.send_command(TM1637_CMD_SET_DATA | TM1637_SET_DATA_F_ADDR)
        self.start()
        self.write(TM1637_CMD_SET_ADDR | seg_pos_list[pos])
        self.write(temp)
        self.stop()
        
        
    def put_str(self, pos, ch):
        for chr in ch:
            self.display(pos, chr, 0)
            pos += 1
