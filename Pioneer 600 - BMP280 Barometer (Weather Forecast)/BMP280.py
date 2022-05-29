from micropython import const
from machine import Pin, I2C


BMP280_I2C_ADDRESS              =    const(0x76)          

#Registers  value
BMP280_ID_Value                      =    const(0x58)
BMP280_RESET_VALUE              =    const(0xB6)

# BMP280 Registers definition  
BMP280_TEMP_XLSB_REG         =    const(0xFC)          
BMP280_TEMP_LSB_REG           =    const(0xFB)         
BMP280_TEMP_MSB_REG         =    const(0xFA)          
BMP280_PRESS_XLSB_REG        =    const(0xF9)        
BMP280_PRESS_LSB_REG          =    const(0xF8)        
BMP280_PRESS_MSB_REG        =    const(0xF7)                              
BMP280_CONFIG_REG              =    const(0xF5)         
BMP280_CTRL_MEAS_REG        =    const(0xF4)       
BMP280_STATUS_REG              =    const(0xF3)         
BMP280_RESET_REG                 =    const(0xE0)         
BMP280_ID_REG                       =    const(0xD0)         

#calibration parameters   
BMP280_DIG_T1_LSB_REG       =    const(0x88)  
BMP280_DIG_T1_MSB_REG     =    const(0x89)  
BMP280_DIG_T2_LSB_REG      =    const(0x8A)  
BMP280_DIG_T2_MSB_REG    =    const(0x8B)  
BMP280_DIG_T3_LSB_REG      =    const(0x8C)  
BMP280_DIG_T3_MSB_REG    =    const(0x8D)  
BMP280_DIG_P1_LSB_REG      =    const(0x8E)  
BMP280_DIG_P1_MSB_REG    =    const(0x8F)  
BMP280_DIG_P2_LSB_REG      =    const(0x90)  
BMP280_DIG_P2_MSB_REG    =    const(0x91)
BMP280_DIG_P3_LSB_REG      =    const(0x92)  
BMP280_DIG_P3_MSB_REG    =    const(0x93)  
BMP280_DIG_P4_LSB_REG      =    const(0x94)  
BMP280_DIG_P4_MSB_REG    =    const(0x95)  
BMP280_DIG_P5_LSB_REG      =    const(0x96)  
BMP280_DIG_P5_MSB_REG    =    const(0x97)  
BMP280_DIG_P6_LSB_REG      =    const(0x98)  
BMP280_DIG_P6_MSB_REG    =    const(0x99)  
BMP280_DIG_P7_LSB_REG      =    const(0x9A)  
BMP280_DIG_P7_MSB_REG    =    const(0x9B)  
BMP280_DIG_P8_LSB_REG      =    const(0x9C)  
BMP280_DIG_P8_MSB_REG    =    const(0x9D)  
BMP280_DIG_P9_LSB_REG      =    const(0x9E)  
BMP280_DIG_P9_MSB_REG    =    const(0x9F)

ELEVATION                             =    const(4)


class BMP280():
    def __init__(self, _i2c):
        self.i2c = _i2c
        self.i2c_address = BMP280_I2C_ADDRESS
        self.t_fine = 0
        
        if (self.read_byte(BMP280_ID_REG) == BMP280_ID_Value):
            self.load_calibration_data()
            self.write_byte(BMP280_CTRL_MEAS_REG, 0xFF)
            self.write_byte(BMP280_CONFIG_REG, 0x14)
            
        else:
            print("BMP280 error!")
        

    def write_byte(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(self.i2c_address, reg, value)


    def read_byte(self, reg):
        retval = self.i2c.readfrom_mem(self.i2c_address, reg, 1)    
        return retval[0]


    def read_word(self, reg):
        value = self.i2c.readfrom_mem(self.i2c_address, reg, 2)    
        return ((value[1] << 8) | value[0])

    
    def read_signed_word(self, reg):
        RES = self.read_word(reg)
        
        if (RES > 32767):
            RES -= 65536

        return RES

    
    def load_calibration_data(self):
        # Temperature Calibration Parameters
        self.dig_T1 = self.read_word(BMP280_DIG_T1_LSB_REG)
        self.dig_T2 = self.read_signed_word(BMP280_DIG_T2_LSB_REG)
        self.dig_T3 = self.read_signed_word(BMP280_DIG_T3_LSB_REG)

        # Barometeric Pressure Calibration Parameters
        self.dig_P1 = self.read_word(BMP280_DIG_P1_LSB_REG)
        self.dig_P2 = self.read_signed_word(BMP280_DIG_P2_LSB_REG)
        self.dig_P3 = self.read_signed_word(BMP280_DIG_P3_LSB_REG)
        self.dig_P4 = self.read_signed_word(BMP280_DIG_P4_LSB_REG)
        self.dig_P5 = self.read_signed_word(BMP280_DIG_P5_LSB_REG)
        self.dig_P6 = self.read_signed_word(BMP280_DIG_P6_LSB_REG)
        self.dig_P7 = self.read_signed_word(BMP280_DIG_P7_LSB_REG)
        self.dig_P8 = self.read_signed_word(BMP280_DIG_P8_LSB_REG)
        self.dig_P9 = self.read_signed_word(BMP280_DIG_P9_LSB_REG)


    def compensate_temperature(self, adc_T):
        var1 = ((adc_T) / 16384.0 - (self.dig_T1) / 1024.0) * (self.dig_T2)
        var2 = (((adc_T) / 131072.0 - (self.dig_T1) / 8192.0)  * ((adc_T) / 131072.0  - (self.dig_T1) / 8192.0)) * (self.dig_T3)
        self.t_fine = var1 + var2
        temperature = (var1 + var2) / 5120.0
        return temperature


    def compensate_pressure(self,adc_P):
        var1 = (self.t_fine / 2.0) - 64000.0
        var2 = var1 * var1 * (self.dig_P6) / 32768.0
        var2 = var2 + var1 * (self.dig_P5) * 2.0
        var2 = (var2 / 4.0) + ((self.dig_P4) * 65536.0) 
        var1 = ((self.dig_P3) * var1 * var1 / 524288.0  + (self.dig_P2) * var1) / 524288.0 
        var1 = (1.0 + var1 / 32768.0) * (self.dig_P1) 

        if var1 == 0.0: 
            return 0 # avoid exception caused by division by zero  

        pressure = 1048576.0 - adc_P
        pressure = (pressure - (var2 / 4096.0)) * 6250.0 / var1
        var1 = (self.dig_P9) * pressure * pressure / 2147483648.0
        var2 = pressure * (self.dig_P8) / 32768.0  
        pressure = pressure + (var1 + var2 + (self.dig_P7)) / 16.0

        return pressure
    

    def get_temperature(self):
        xlsb = self.read_byte(BMP280_TEMP_XLSB_REG)
        lsb =  self.read_byte(BMP280_TEMP_LSB_REG)
        msb =  self.read_byte(BMP280_TEMP_MSB_REG)

        adc_T = (msb << 12) | (lsb << 4) | (xlsb >> 4)
        temperature = self.compensate_temperature(adc_T)

        return temperature # temperature in deg. C


    def get_pressure(self):
        xlsb = self.read_byte(BMP280_PRESS_XLSB_REG)
        lsb =  self.read_byte(BMP280_PRESS_LSB_REG) 
        msb =  self.read_byte(BMP280_PRESS_MSB_REG) 

        adc_P = (msb << 12) | (lsb << 4) | (xlsb >> 4)
        pressure = self.compensate_pressure(adc_P)
        
        pressure = (pressure / 100.0)
        pressure =  (pressure + (ELEVATION / 9.2))
        
        return pressure #pressure in mbar



