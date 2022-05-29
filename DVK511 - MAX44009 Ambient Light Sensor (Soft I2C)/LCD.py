from machine import Pin
from utime import sleep_ms
from micropython import const

clear_display = const(0x01)                
goto_home = const(0x02)                                                    
         
cursor_direction_inc = const(0x06)    
cursor_direction_dec = const(0x04)
display_shift = const(0x05) 
display_no_shift = const(0x04)

display_on = const(0x0C)
display_off = const(0x0A)       
cursor_on = const(0x0A)               
cursor_off = const(0x08)       
blink_on = const(0x09)   
blink_off = const(0x08)         
                                    
_8_pin_interface = const(0x30)  
_4_pin_interface = const(0x20)      
_2_row_display = const(0x28) 
_1_row_display = const(0x20)
_5x10_dots = const(0x60)                                                                                        
_5x7_dots = const(0x20)
                                   
line_1_y_pos = const(0x00)
line_2_y_pos = const(0x40) 
line_3_y_pos = const(0x14)
line_4_y_pos = const(0x54)

dly = const(2)

DAT = const(1)
CMD = const(0)


class LCD():
    def __init__(self, RS, EN, D4, D5, D6, D7):
        self.rs = Pin(RS, Pin.OUT)
        self.en = Pin(EN, Pin.OUT)
        self.d4 = Pin(D4, Pin.OUT)
        self.d5 = Pin(D5, Pin.OUT)
        self.d6 = Pin(D6, Pin.OUT)
        self.d7 = Pin(D7, Pin.OUT)
                
        self.init()
        
        
    def write(self, value, mode):
        self.rs.value(mode)
        self.send(value)
        
        
    def send(self, value):
        self.d7.value(0x01 & (value >> 0x07))
        self.d6.value(0x01 & (value >> 0x06))
        self.d5.value(0x01 & (value >> 0x05))
        self.d4.value(0x01 & (value >> 0x04))        
        self.toggle_en()
        self.d7.value(0x01 & (value >> 0x03))
        self.d6.value(0x01 & (value >> 0x02))
        self.d5.value(0x01 & (value >> 0x01))
        self.d4.value(0x01 & value)        
        self.toggle_en()
        
        
    def toggle_en(self):
        self.en.value(1)
        sleep_ms(dly)
        self.en.value(0)
        sleep_ms(dly)
        
        
    def clear_home(self):
        self.write(clear_display, CMD)
        self.write(goto_home, CMD)
        
        
    def goto_xy(self, x_pos, y_pos):
        if(y_pos == 1):
            self.write((0x80 | (line_2_y_pos + x_pos)), CMD)
            
        elif(y_pos == 2):
            self.write((0x80 | (line_3_y_pos + x_pos)), CMD)
            
        elif(y_pos == 3):
            self.write((0x80 | (line_4_y_pos + x_pos)), CMD)
            
        else:
            self.write((0x80 | (line_1_y_pos + x_pos)), CMD)
        
        
    def init(self):
        sleep_ms(dly)
        self.toggle_en()
        self.write(0x33, CMD)
        self.write(0x32, CMD)
        
        self.write((_4_pin_interface | _2_row_display | _5x7_dots), CMD)
        self.write((display_on | cursor_off | blink_off), CMD)
        self.write(clear_display, CMD)
        self.write((cursor_direction_inc | display_no_shift), CMD)
        
        
    def put_chr(self, ch):
        self.write(ord(ch), DAT)
        
        
    def put_str(self, ch_string):
        for chr in ch_string:
            self.put_chr(chr)

