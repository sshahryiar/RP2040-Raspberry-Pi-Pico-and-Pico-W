from micropython import const
from utime import sleep_ms
import math


HMC5883L_I2C_address = const(0x1E)

HMC5883L_Config_Reg_A = const(0x00)
HMC5883L_Config_Reg_B = const(0x01)
HMC5883L_Mode_Reg = const(0x02)
HMC5883L_X_MSB_Reg = const(0x03)
HMC5883L_X_LSB_Reg = const(0x04)
HMC5883L_Z_MSB_Reg = const(0x05)
HMC5883L_Z_LSB_Reg = const(0x06)
HMC5883L_Y_MSB_Reg = const(0x07)
HMC5883L_Y_LSB_Reg = const(0x08)
HMC5883L_Status_Reg = const(0x09)
HMC5883L_ID_Reg_A = const(0x0A)             
HMC5883L_ID_Reg_B = const(0x0B) 
HMC5883L_ID_Reg_C = const(0x0C)
       
HMC5883L_declination_angle =  -0.5167


class HMC5883L():
    def __init__(self, _i2c):
        self.m_scale = 1.3
        
        self.i2c = _i2c
        
        self.init()
        
        
    def init(self):
        self.write(HMC5883L_Config_Reg_A, 0x70)
        self.write(HMC5883L_Config_Reg_B, 0xA0)
        self.write(HMC5883L_Mode_Reg, 0x00)
        self.set_scale(self.m_scale)
        
        
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(HMC5883L_I2C_address, reg, value)
        
        
    def read_byte(self, reg):
        retval = self.i2c.readfrom_mem(HMC5883L_I2C_address, reg, 0x01)    
        return retval[0x00]
    
    
    def read_word(self, reg):
        value = self.i2c.readfrom_mem(HMC5883L_I2C_address, reg, 0x02)
        
        retval = value[0x00]
        retval <<= 0x08
        retval |= value[0x01]
        
        return retval
    
    
    def read_signed_word(self, address):
        retval = self.read_word(address)
        
        if(retval > 32767):
            retval -= 65536
            
        return retval
    
    
    def set_scale(self, gauss):
        if (gauss == 0.88):
            value = 0x00
            self.m_scale = 0.73
            
        elif (gauss == 1.3):
            value = 0x01
            self.m_scale = 0.92
            
        elif (gauss == 1.9):
            value = 0x02
            self.m_scale = 1.22
            
        elif (gauss == 2.5):
            value = 0x03
            self.m_scale = 1.52
            
        elif (gauss == 4.0):
            value = 0x04
            self.m_scale = 2.27
            
        elif (gauss == 4.7):
            value = 0x05
            self.m_scale = 2.56
            
        elif (gauss == 5.6):
            value = 0x06
            self.m_scale = 3.03
            
        elif (gauss == 8.1):
            value = 0x07
            self.m_scale = 4.35
            
        value = (value << 0x05)
        self.write(HMC5883L_Config_Reg_B, value)
        
        
    def get_raw_data(self):
        x_axis = (float(self.read_signed_word(HMC5883L_X_MSB_Reg)) * self.m_scale)
        z_axis = (float(self.read_signed_word(HMC5883L_Z_MSB_Reg)) * self.m_scale)
        y_axis = (float(self.read_signed_word(HMC5883L_Y_MSB_Reg)) * self.m_scale)
                
        return x_axis, y_axis, z_axis
        
        
    def get_heading(self):
        x_axis, y_axis, z_axis = self.get_raw_data()
        h = math.atan2(y_axis, x_axis)
        h += HMC5883L_declination_angle
        h = (h * (180.0 / math.pi))
        
        if(h < 0.0):
            h += 360
            
        if(h > 360):
            h -= 360

        return h

