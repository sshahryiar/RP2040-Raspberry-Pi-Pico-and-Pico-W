from machine import Pin
from utime import sleep_us


leds = [
 0x0000,
 0x0001,
 0x0002,
 0x0004,
 0x0008,
 0x0010,
 0x0020,
 0x0040,
 0x0080,
 0x0100,
 0x0200,
 0x0400,
 0x0800,
 0x1000,
 0x2000,
 0x4000,
 0x8000
]


class LED_circle():
    def __init__(self, _sdi, _sck, _cs, _mr):
        self.mr = Pin(_mr, Pin.OUT)
        self.cs = Pin(_cs, Pin.OUT)
        self.sck = Pin(_sck, Pin.OUT)
        self.sdi = Pin(_sdi, Pin.OUT)
        
        self.mr.high()
        self.cs.low()
        self.sck.low()
        self.sdi.low()
        
    
    def update(self):
        self.cs.high()
        sleep_us(100)
        self.cs.low()
        
    
    def write(self, value):
        for i in range(0, 8):
            self.sck.low()
            
            if((value & 0x80) != 0x00):
                self.sdi.high()
            else:
                self.sdi.low()
                
            self.sck.high()
            value <<= 0x01
    
    
    def send(self, value, disp_type):
        if(value > 16):
            value = 16
        
        if(value < 0):
            value = 0
            
        temp = leds[value]
        
        if(disp_type == True):
            temp = ~temp
        
        lb = (temp & 0x00FF)
        hb = ((temp & 0xFF00) >> 0x08)
        
        self.write(lb)
        self.write(hb)
        
        self.update()
