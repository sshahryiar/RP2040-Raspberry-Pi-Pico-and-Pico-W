from micropython import const
from machine import Pin
from utime import sleep_ms


BME280_REGISTER_CHIPID = const(0xD0)
BME280_REGISTER_VERSION = const(0xD1)
BME280_REGISTER_SOFTRESET = const(0xE0)

BME280_REGISTER_CAL00 = const(0x88)
BME280_REGISTER_CAL01 = const(0x89)
BME280_REGISTER_CAL02 = const(0x8A)
BME280_REGISTER_CAL03 = const(0x8B)
BME280_REGISTER_CAL04 = const(0x8C)
BME280_REGISTER_CAL05 = const(0x8D)
BME280_REGISTER_CAL06 = const(0x8E)
BME280_REGISTER_CAL07 = const(0x8F)
BME280_REGISTER_CAL08  = const(0x90)
BME280_REGISTER_CAL09 = const(0x91)
BME280_REGISTER_CAL10 = const(0x92)
BME280_REGISTER_CAL11 = const(0x93)
BME280_REGISTER_CAL12 = const(0x94)
BME280_REGISTER_CAL13 = const(0x95)
BME280_REGISTER_CAL14 = const(0x96)
BME280_REGISTER_CAL15 = const(0x97)
BME280_REGISTER_CAL16 = const(0x98)
BME280_REGISTER_CAL17 = const(0x99)
BME280_REGISTER_CAL18 = const(0x9A)
BME280_REGISTER_CAL19 = const(0x9B)
BME280_REGISTER_CAL20 = const(0x9C)
BME280_REGISTER_CAL21 = const(0x9D)
BME280_REGISTER_CAL22 = const(0x9E)
BME280_REGISTER_CAL23 = const(0x9F)
BME280_REGISTER_CAL24 = const(0xA0)
BME280_REGISTER_CAL25 = const(0xA1)
BME280_REGISTER_CAL26 = const(0xE1)
BME280_REGISTER_CAL27 = const(0xE2)
BME280_REGISTER_CAL28 = const(0xE3)
BME280_REGISTER_CAL29 = const(0xE4)
BME280_REGISTER_CAL30 = const(0xE5)
BME280_REGISTER_CAL31 = const(0xE6)
BME280_REGISTER_CAL32 = const(0xE7)
BME280_REGISTER_CAL33 = const(0xE8)
BME280_REGISTER_CAL34 = const(0xE9)
BME280_REGISTER_CAL35 = const(0xEA)
BME280_REGISTER_CAL36 = const(0xEB)
BME280_REGISTER_CAL37 = const(0xEC)
BME280_REGISTER_CAL38 = const(0xED)
BME280_REGISTER_CAL39 = const(0xEE)
BME280_REGISTER_CAL40 = const(0xEF)
BME280_REGISTER_CAL41 = const(0xF0)
BME280_REGISTER_CONTROLHUMID = const(0xF2)
BME280_REGISTER_STATUS = const(0xF3)
BME280_REGISTER_CONTROL = const(0xF4)
BME280_REGISTER_CONFIG = const(0xF5)
BME280_REGISTER_PRESSUREDATA = const(0xF7)
BME280_REGISTER_TEMPDATA = const(0xFA)
BME280_REGISTER_HUMIDDATA = const(0xFD)

BME280_DIG_T1_REG = BME280_REGISTER_CAL00
BME280_DIG_T2_REG = BME280_REGISTER_CAL02
BME280_DIG_T3_REG = BME280_REGISTER_CAL04

BME280_DIG_P1_REG = BME280_REGISTER_CAL06
BME280_DIG_P2_REG = BME280_REGISTER_CAL08
BME280_DIG_P3_REG = BME280_REGISTER_CAL10
BME280_DIG_P4_REG = BME280_REGISTER_CAL12
BME280_DIG_P5_REG = BME280_REGISTER_CAL14
BME280_DIG_P6_REG = BME280_REGISTER_CAL16
BME280_DIG_P7_REG = BME280_REGISTER_CAL18
BME280_DIG_P8_REG = BME280_REGISTER_CAL20
BME280_DIG_P9_REG = BME280_REGISTER_CAL22
    
BME280_DIG_H1_REG = BME280_REGISTER_CAL25
BME280_DIG_H2_REG = BME280_REGISTER_CAL26
BME280_DIG_H3_REG = BME280_REGISTER_CAL28
BME280_DIG_H4_REG = BME280_REGISTER_CAL29
BME280_DIG_H5_REG = BME280_REGISTER_CAL30
BME280_DIG_H6_REG = BME280_REGISTER_CAL32

BME280_OSAMPLE_1 = const(0x01)
BME280_OSAMPLE_2 = const(0x02)
BME280_OSAMPLE_4 = const(0x03)
BME280_OSAMPLE_8 = const(0x04)
BME280_OSAMPLE_16 = const(0x05)


calibration_dig_T1 = 0
calibration_dig_T2 = 0
calibration_dig_T3 = 0

calibration_dig_P1 = 0
calibration_dig_P2 = 0
calibration_dig_P3 =0
calibration_dig_P4 = 0
calibration_dig_P5 = 0
calibration_dig_P6 = 0
calibration_dig_P7 = 0
calibration_dig_P8 = 0
calibration_dig_P9 = 0

calibration_dig_H1 = 0
calibration_dig_H2 = 0
calibration_dig_H3 = 0
calibration_dig_H4 = 0
calibration_dig_H5 = 0
calibration_dig_H6 = 0


class BME280_SPI():
    def __init__(self, _spi, _csn):
        self.spi = _spi
        self.csn = Pin(_csn, Pin.OUT)
        self.t_fine = 0
        
        self.init()
        
        
    def init(self):
        self.write(BME280_REGISTER_SOFTRESET, 0xB6)
        sleep_ms(300)
        
        while(self.calibration_read_status() == True):
            sleep_ms(100)
            
        self.read_coefficients()
        self.write(BME280_REGISTER_CONTROLHUMID, 0x01)
        self.write(BME280_REGISTER_CONTROL, 0x3F)
        
        
    def write(self, address, value):
        self.csn.off()
        self.spi.write(bytearray([address & 0x7F]))
        self.spi.write(bytearray([value]))
        self.csn.on()
        
        
    def read_byte(self, address):
        retval = 0
        self.csn.off()
        self.spi.write(bytearray([address | 0x80]))
        retval = self.spi.read(0x01, address)
        self.csn.on()
        return retval[0]
    
    
    def read_signed_byte(self, address):
        retval = self.read_byte(address)
        
        if(retval > 127):
            retval -= 256
            
        return retval
    
    
    def read_word(self, address):
        value = 0
        retval = 0
        self.csn.off()
        self.spi.write(bytearray([address | 0x80]))
        value = self.spi.read(0x02, address)
        self.csn.on()
        retval = ((value[0x00] << 0x08) | value[0x01])
        return retval
    
    
    def read_signed_word(self, address):
        retval = self.read_word(address)
        
        if(retval > 32767):
            retval -= 65536
            
        return retval
        
    
    def read_long(self, address):
        value = 0
        retval = 0
        self.csn.off()
        self.spi.write(bytearray([address | 0x80]))
        value = self.spi.read(0x03, address)
        self.csn.on()
        retval = ((value[0x00] << 16) | (value[0x01] << 8) | value[0x02])
        return retval
    
    
    def read_word_little_endian(self, address):
        temp = self.read_word(address)
        return ((temp >> 0x08) + ((temp << 0x08) & 0xFF00))
    
    
    def read_signed_word_little_endian(self, address):
        retval = 0
        retval = self.read_word_little_endian(address)
        if(retval > 32767):
            retval -= 65536
        
        return retval
        

    def calibration_read_status(self):
        status = self.read_byte(BME280_REGISTER_STATUS)
        return ((status & (0x01 << 0x00)) != 0x00)
    
    
    def read_coefficients(self):
        global calibration_dig_T1, calibration_dig_T2, calibration_dig_T3
        global calibration_dig_P1, calibration_dig_P2, calibration_dig_P3
        global calibration_dig_P4, calibration_dig_P5, calibration_dig_P6
        global calibration_dig_P7, calibration_dig_P8, calibration_dig_P9
        global calibration_dig_H1, calibration_dig_H2, calibration_dig_H3
        global calibration_dig_H4, calibration_dig_H5, calibration_dig_H6
        
        calibration_dig_T1 = self.read_word_little_endian(BME280_DIG_T1_REG)
        calibration_dig_T2 = self.read_signed_word_little_endian(BME280_DIG_T2_REG)
        calibration_dig_T3 = self.read_signed_word_little_endian(BME280_DIG_T3_REG)
        
        calibration_dig_P1 = self.read_word_little_endian(BME280_DIG_P1_REG)
        calibration_dig_P2 = self.read_signed_word_little_endian(BME280_DIG_P2_REG)
        calibration_dig_P3 = self.read_signed_word_little_endian(BME280_DIG_P3_REG)
        calibration_dig_P4 = self.read_signed_word_little_endian(BME280_DIG_P4_REG)
        calibration_dig_P5 = self.read_signed_word_little_endian(BME280_DIG_P5_REG)
        calibration_dig_P6 = self.read_signed_word_little_endian(BME280_DIG_P6_REG)
        calibration_dig_P7 = self.read_signed_word_little_endian(BME280_DIG_P7_REG)
        calibration_dig_P8 = self.read_signed_word_little_endian(BME280_DIG_P8_REG)
        calibration_dig_P9 = self.read_signed_word_little_endian(BME280_DIG_P9_REG)
        
        calibration_dig_H1 = self.read_byte(BME280_DIG_H1_REG)
        calibration_dig_H2 = self.read_signed_word_little_endian(BME280_DIG_H2_REG)
        calibration_dig_H3 = self.read_byte(BME280_DIG_H3_REG)
        calibration_dig_H4 = ((self.read_byte(BME280_DIG_H4_REG) << 0x04) + (self.read_byte(BME280_DIG_H4_REG + 0x01)  & 0x0F))
        calibration_dig_H5 = ((self.read_byte(BME280_DIG_H5_REG + 0x01) << 0x04) + (self.read_byte(BME280_DIG_H5_REG) >> 0x04))
        calibration_dig_H6 = self.read_byte(BME280_DIG_H6_REG)
        
        
    def get_T(self):
        global calibration_dig_T1, calibration_dig_T2, calibration_dig_T3
        
        tmp = 0
        adc_T = 0
        temp1 = 0
        temp2 = 0        
        
        adc_T = (self.read_long(BME280_REGISTER_TEMPDATA) >> 0x04)
        
        temp1 = (((((adc_T >> 3) - (calibration_dig_T1 << 1))) * (calibration_dig_T2)) >> 11)
        temp2 = ((((((adc_T >> 4) - (calibration_dig_T1)) * ((adc_T >> 4) - (calibration_dig_T1))) >> 12) * (calibration_dig_T3)) >> 14)
        
        self.t_fine = (temp1 + temp2)
        tmp = (((self.t_fine * 5) + 128) >> 8)
        tmp /= 100.0
        
        return tmp
        
        
    def get_P(self):
        global calibration_dig_P1, calibration_dig_P2, calibration_dig_P3
        global calibration_dig_P4, calibration_dig_P5, calibration_dig_P6
        global calibration_dig_P7, calibration_dig_P8, calibration_dig_P9
        
        tmp = 0
        pres = 0
        temp1 = 0
        temp2 = 0
        adc_P = 0
        
        adc_P = (self.read_long(BME280_REGISTER_PRESSUREDATA) >> 0x04)
        
        temp1 = (self.t_fine - 128000)        
        temp2 = (temp1 * temp1 * calibration_dig_P6)
        temp2 = (temp2 + ((temp1 * calibration_dig_P5) << 17))
        temp2 = (temp2 + ((calibration_dig_P4) << 35))
        
        temp1 = ((((temp1 * temp1) * calibration_dig_P3) >> 8) + ((temp1 * calibration_dig_P2) >> 12))
        temp1 = ((((1 << 47) + temp1)) * (calibration_dig_P1) >> 33)
        
        if(temp1 == 0):
            return  0
            
        tmp = (1048576 - adc_P)
        tmp = ((((tmp << 31) - temp2) * 3125) // temp1)
        
        temp1 = (((calibration_dig_P9) * (tmp >> 13) * (tmp >> 13)) >> 25)
        temp2 = (((calibration_dig_P8) * tmp) >> 19)
        
        tmp = (((tmp + temp1 + temp2) >> 8) + ((calibration_dig_P7) << 4))
        
        pres = (tmp / 256.0)
        pres /= 100.0
        
        return pres
    
    
    def get_RH(self):
        global calibration_dig_H1, calibration_dig_H2, calibration_dig_H3
        global calibration_dig_H4, calibration_dig_H5, calibration_dig_H6
        
        rh = 0
        adc_RH = 0
        h = 0
        
        adc_RH = self.read_word(BME280_REGISTER_HUMIDDATA)
        h = (self.t_fine - 76800)
        
        h = (((((adc_RH << 14) - ((calibration_dig_H4) << 20) - ((calibration_dig_H5) * h)) + (16384)) >> 15) * (((((((h * (calibration_dig_H6)) >> 10)
                            * (((h * (calibration_dig_H3)) >> 11) + 32768)) >> 10) + 2097152) * (calibration_dig_H2) + 8192) >> 14))
        
        h = (h - (((((h >> 15) * (h >> 15)) >> 7) * (calibration_dig_H1)) >> 4))
        
        if(h < 0):
            h = 0
            
        if(h > 419430400):
            h = 419430400
      
        adc_RH = (h >> 12)
        rh = (adc_RH / 1024.0)
        
        return rh
