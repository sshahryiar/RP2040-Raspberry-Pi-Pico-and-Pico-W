from micropython import const
from machine import Pin, SPI


XPT2046_CS_pin = const(16)
XPT2046_IRQ_pin = const(17)
XPT2046_SCK_pin = const(10)
XPT2046_MOSI_pin = const(11)
XPT2046_MISO_pin = const(12)


XPT2046_CMD_RDY = const(0x90)
XPT2046_CMD_RDX = const(0xD0)

XPT2046_l_max = const(319)
XPT2046_w_max = const(239)


class touch():
    def __init__(self):
        
        self.x_axis_min = 511
        self.x_axis_max = 4095
        self.y_axis_min = 4095
        self.y_axis_max = 511
        
        self.XPT2046_CS = Pin(XPT2046_CS_pin, Pin.OUT)
        self.XPT2046_SCK = Pin(XPT2046_SCK_pin, Pin.OUT)
        self.XPT2046_IRQ = Pin(XPT2046_IRQ_pin, Pin.IN)
        self.XPT2046_MISO = Pin(XPT2046_MISO_pin, Pin.IN)
        self.XPT2046_MOSI = Pin(XPT2046_MOSI_pin, Pin.OUT)
        
        self.XPT2046_SPI = SPI(1, 10_000_000, polarity = False, phase = False, sck = self.XPT2046_SCK, mosi = self.XPT2046_MOSI, miso = self.XPT2046_MISO)

    
    def read_word(self):
        retval = self.XPT2046_SPI.read(0x02, 0x00)
        return (((retval[0] << 0x08) | retval[1]) >> 3)
    
    
    def map_value(self, v, x_min, x_max, y_min, y_max):
        return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


    def contrain(self, value, min_value, max_value):
        if(value > max_value):
            return max_value
        
        elif(value < min_value):
            return min_value
        
        else:
            return value
       
       
    def read_coordinates(self):
        avg_x = 0
        avg_y = 0
        samples = 4
        
        self.XPT2046_CS.off()
        
        while(samples > 0):
            self.XPT2046_SPI.write(bytearray([XPT2046_CMD_RDY]))
            avg_x += self.read_word()
            
            self.XPT2046_SPI.write(bytearray([XPT2046_CMD_RDX]))
            avg_y += self.read_word()
            
            samples -= 1
        
        self.XPT2046_CS.on()
        
        avg_y >>= 2
        avg_x >>= 2
        
        return avg_x, avg_y
    
    
    def get_xy(self):
        x_val, y_val = self.read_coordinates()
        
        x_value = self.map_value(x_val, self.x_axis_min, self.x_axis_max, 0, XPT2046_l_max) 
        y_value = self.map_value(y_val, self.y_axis_min, self.y_axis_max, 0, XPT2046_w_max)
        
        x_val = self.contrain(x_value, 0, XPT2046_l_max) 
        y_val = self.contrain(y_value, 0, XPT2046_w_max)
        
        return x_val, y_val
    
    
    def calibration(self, x_min, y_min, x_max, y_max):
        self.x_axis_min = x_min
        self.x_axis_max = x_max
        self.y_axis_min = y_min
        self.y_axis_max = y_max       
        