from micropython import const
from machine import Pin
from utime import sleep_ms, sleep_us


MPL115A1_PRESH = const(0x80)
MPL115A1_PRESL = const(0x82)
MPL115A1_TEMPH = const(0x84)
MPL115A1_TEMPL = const(0x86)

MPL115A1_A0_H = const(0x88)                                                
MPL115A1_A0_L = const(0x8A)
MPL115A1_B1_H = const(0x8C)
MPL115A1_B1_L = const(0x8E)
MPL115A1_B2_H = const(0x90)             
MPL115A1_B2_L = const(0x92)
MPL115A1_C12_H = const(0x94)
MPL115A1_C12_L = const(0x96)                   

MPL115A1_conv_cmd = const(0x24)


coefficient_A0 = 0
coefficient_B1 = 0
coefficient_B2 = 0
coefficient_C12 = 0


class MPL115A1():
    def __init__(self, _spi, _csn, _sdn):
        self.spi = _spi
        self.csn = Pin(_csn, Pin.OUT)
        self.sdn = Pin(_sdn, Pin.OUT)
        
        self.init()
        
        
    def init(self):
        self.sdn.on()
        self.csn.on()
        self.load_coefficients()
        
        
    def load_coefficients(self):
        global coefficient_A0, coefficient_B1, coefficient_B2, coefficient_C12
        
        HB = 0
        LB = 0
        
        HB, LB = self.read_word(MPL115A1_A0_H)
        coefficient_A0 = ((HB << 0x05) + (LB >> 0x03) + (float(LB & 0x07) / 8.0))
                          
        HB, LB = self.read_word(MPL115A1_B1_H)
        coefficient_B1 = (((float((HB & 0x1F) * 0x0100) + LB) / 8192.0) - 3.0)
                          
        HB, LB = self.read_word(MPL115A1_B2_H)
        coefficient_B2 = ((float(((HB - 0x80) << 8) + LB) / 16384.0) - 2.0)
        
        HB, LB = self.read_word(MPL115A1_C12_H)
        coefficient_C12 = (float((HB * 0x100) + LB) / 16777216.0)
                          
        
    def write(self, address, value):
        self.csn.off()
        sleep_ms(3)
        self.spi.write(bytearray([address & 0x7F]))
        self.spi.write(bytearray([value]))
        self.csn.on()
        
        
    def read_byte(self, address):
        value = 0
        self.csn.off()
        sleep_ms(3)
        self.spi.write(bytearray([address]))
        value = self.spi.read(0x02, address)
        self.csn.on()
        
        return value[0]
    
    
    def read_word(self, address):
        HB = self.read_byte(address)
        LB = self.read_byte(address + 0x02)
        
        return HB, LB
                          
                          
    def get_data(self):
        global coefficient_A0, coefficient_B1, coefficient_B2, coefficient_C12
        
        HB = 0
        LB = 0
        P_adc = 0
        T_adc = 0
        pressure = 0
        temperature = 0
        
        self.write(MPL115A1_conv_cmd, 0x00)
        
        HB, LB = self.read_word(MPL115A1_PRESH)
        P_adc = (((HB << 0x08) + LB) >> 0x06)
        
        HB, LB = self.read_word(MPL115A1_TEMPH)
        T_adc = (((HB << 0x08) + LB) >> 0x06)
        
        pressure = ( coefficient_A0 + (( coefficient_B1 + ( coefficient_C12 * T_adc)) * P_adc) + ( coefficient_B2 * T_adc))
        pressure = (((pressure * 65.0) / 1023.0) + 50.0)
        
        temperature = (30.0 + ((T_adc - 472) / (-5.35)))
        
        return pressure, temperature
