from micropython import const
from machine import Pin

mosi_pin = const(11)
sck_pin = const(10)
rclk_pin = const(9)


seg_code_list = [
    0x3F, # 0
    0x06, # 1
    0x5B, # 2
    0x4F, # 3
    0x66, # 4
    0x6D, # 5
    0x7D, # 6
    0x07, # 7
    0x7F, # 8
    0x6F, # 9
    0x77, # A
    0x7C, # b
    0x39, # C
    0x5E, # d
    0x79, # E
    0x71  # F
]

seg_pos_list = [
    0xFE, # 1st
    0xFD, # 2nd
    0xFB, # 3rd
    0xF7, # 4th  
]


class seg_disp():

    def __init__(self):
        self.mosi = Pin(mosi_pin, Pin.OUT)
        self.sck = Pin(sck_pin, Pin.OUT)
        self.rclk = Pin(rclk_pin, Pin.OUT)

    def send_data(self, value, pos, dot):
        clks = 16
        temp = seg_pos_list[pos]
        temp <<= 8
        temp |=  seg_code_list[value]
        
        if(dot == True):
            temp |= 0x80
                
        self.rclk.value(False)

        while(clks > 0):
            if((temp & 0x8000) != 0x0000):
                self.mosi.value(True)
            else:
                self.mosi.value(False)

            self.sck.value(True)
            temp <<= 1
            clks -= 1
            self.sck.value(False)

        self.rclk.value(True)
