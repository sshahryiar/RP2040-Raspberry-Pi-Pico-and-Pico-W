from machine import I2C


class PCF8574_IO():
    
    def __init__(self, i2c, i2c_addr):        
        self.i2c = i2c
        self.i2c_addr = i2c_addr

    def PCF8574_write_byte(self, value):        
        self.i2c.writeto(self.i2c_addr, bytes([value]))
        
    def PCF8574_read_byte(self, mask):        
        self.PCF8574_write_byte(mask)
        retval = self.i2c.readfrom(self.i2c_addr, 1)        
        return retval[0]
