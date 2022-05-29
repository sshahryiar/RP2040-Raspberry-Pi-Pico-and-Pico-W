from micropython import const
from machine import Pin, SoftI2C
from utime import sleep_ms


MAX44009_address = const(0x4A)
MAX44009_INTERRUPT_STATUS_REG = const(0x00)
MAX44009_INTERRUPT_ENABLE_REG = const(0x01)
MAX44009_CONFIGURATION_REG = const(0x02)
MAX44009_LUX_HIGH_BYTE_REG = const(0x03)
MAX44009_LUX_LOW_BYTE_REG = const(0x04)
MAX44009_UPPER_THRESHOLD_HIGH_BYTE_REG = const(0x05)
MAX44009_LOWER_THRESHOLD_HIGH_BYTE_REG = const(0x06)
MAX44009_THRESHOLD_TIMER_REG = const(0x07)


class MAX44009():
    
    def __init__(self, _i2c, _i2c_address = MAX44009_address):
        self.I2C = _i2c
        self.I2C_address = _i2c_address
        self.init()
        
        
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
            
        self.I2C.writeto_mem(self.I2C_address, reg, value)
        
        
    def read(self, reg):
        return (self.I2C.readfrom_mem(self.I2C_address, reg, 1)[0])
    
    
    def init(self):
        self.write(MAX44009_INTERRUPT_ENABLE_REG, 0x00)
        self.write(MAX44009_CONFIGURATION_REG, 0x03)
        self.write(MAX44009_THRESHOLD_TIMER_REG, 0xFF)
    
    
    def get_lux_value(self):
        HB = 0
        LB = 0
        exponent = 0
        mantisa = 0
        
        HB = self.read(MAX44009_LUX_HIGH_BYTE_REG)
        LB = self.read(MAX44009_LUX_LOW_BYTE_REG)
        
        exponent = ((HB & 0xF0) >> 4)
        mantisa = (((HB & 0x0F) << 4) | (LB & 0x0F))
        
        while(exponent > -1):
            mantisa <<= 1
            exponent -= 1
            
        lx = (float(mantisa) * 0.045)
        return lx
