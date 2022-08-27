#Pin Connections

# RW = GND
# RS = base_pin + 5
# EN = base_pin + 4
# D7 = base_pin + 3
# D6 = base_pin + 2
# D5 = base_pin + 1
# D4 = base_pin + 0


from machine import Pin
from utime import sleep_ms
from rp2 import asm_pio, StateMachine, PIO
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


lcd_value = 0


class LCD():
    
    @asm_pio(out_shiftdir = PIO.SHIFT_RIGHT,
         autopull = True,
         pull_thresh = 6,
         out_init = ((PIO.OUT_HIGH, ) * 6))
    
    def lcd_write():
        pull(ifempty)  # Pull data from TX_FIFO if empty
        out(pins, 6)   # write lcd info
    
    
    def toggle_en(self):
        global lcd_value
        
        lcd_value |= 0x10
        sleep_ms(dly)
        self.sm.put(lcd_value)
        
        lcd_value &= 0x2F
        sleep_ms(dly)
        self.sm.put(lcd_value)
    
    
    def write(self, value, mode):
        global lcd_value
        
        if(mode == DAT):
            lcd_value |= 0x20
        else:
            lcd_value &= 0x1F
            
        self.send(value)
    
    
    def send(self, value):
        global lcd_value
        
        temp = ((value & 0xF0) >> 4)
        lcd_value &= 0x30
        lcd_value |= (temp & 0x0F)
        self.toggle_en()
        
        temp = (value & 0x0F)
        lcd_value &= 0x30
        lcd_value |= (temp & 0x0F)
        self.toggle_en()
        
        
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

        
    def __init__(self, base_pin):
        self.out_pin = Pin(base_pin, Pin.OUT)
        self.sm = StateMachine(0, LCD.lcd_write, out_base = self.out_pin, freq = 250000)
        self.sm.active(1)
        self.init()

