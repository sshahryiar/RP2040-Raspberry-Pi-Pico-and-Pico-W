from machine import I2C


class PCF8574():
    
    def __init__(self, _i2c, _i2c_addr = 0x20):        
        self.i2c = _i2c
        self.i2c_addr = _i2c_addr
        self.tmp = 0
        
    
    def port_read(self, mask):
        self.write(mask | self.read())
        return self.read()
    
    
    def port_write(self, value):
        self.write(value & 0xFF)
        
        
    def pin_read(self, pin):
        return ((self.read() >> pin) & 0x01)
    
    
    def pin_write(self, pin, value):
        if(value != 0):
            tmp = 0x00
            tmp |= (1 << pin)
            tmp |= self.read()
        
        else:
            tmp = 0xFF
            tmp &= ~(1 << pin)
            tmp &= self.read()
            
        self.write(tmp)
        
        
    def pin_toggle(self, pin):
        self.tmp ^= 0x01
        self.pin_write(pin, self.tmp)
        
        
    def read(self):             
        return self.i2c.readfrom(self.i2c_addr, 1)[0]
    
    
    def write(self, value):
        self.i2c.writeto(self.i2c_addr, bytes([value]))
         

