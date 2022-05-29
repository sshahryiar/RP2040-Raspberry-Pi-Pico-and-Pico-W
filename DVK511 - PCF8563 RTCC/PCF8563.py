from micropython import const
from machine import Pin, I2C


PCF8563_I2C_address = const(0x51)
                
PCF8563_TIMER = const(0x0F)    
PCF8563_CONTROL1 = const(0x00)     
PCF8563_CONTROL2 = const(0x01)                                                                
PCF8563_SECOND = const(0x02)    
PCF8563_MINUTE = const(0x03)     
PCF8563_HOUR = const(0x04)    
PCF8563_DATE = const(0x05)     
PCF8563_DAY = const(0x06)
PCF8563_MONTH = const(0x07)                   
PCF8563_YEAR = const(0x08) 
PCF8563_ALARM_MINUTE = const(0x09)  
PCF8563_ALARM_HOUR = const(0x0A)  
PCF8563_ALARM_DAY = const(0x0B)  
PCF8563_ALARM_WEEKDAY = const(0x0C)   
PCF8563_CLKOUT = const(0x0D)     
PCF8563_TCONTROL = const(0x0E)


class PCF8563():
    def __init__(self, _i2c):
        self.alarm_on = const(0x00)
        self.alarm_off = const(0x01)
        self.i2c = _i2c
        self.i2c_address = PCF8563_I2C_address
        
        self.init()
        
        
    def init(self):
        self.stop_RTC()
        self.clear_alarm()
        self.start_RTC()
        
        
    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(self.i2c_address, reg, value)
        
        
    def read(self, reg):
        retval = self.i2c.readfrom_mem(self.i2c_address, reg, 1)    
        return retval[0]
    
    
    def bcd_to_decimal(self, value):
        return ((value & 0x0F) + (((value & 0xF0) >> 0x04) * 0x0A))


    def decimal_to_bcd(self, value):
        return (((value // 0x0A) << 0x04) & 0xF0) | ((value % 0x0A) & 0x0F)
    
    
    def stop_RTC(self):
        self.write(PCF8563_CONTROL1, 0x28)
        
    
    def start_RTC(self):
        self.write(PCF8563_CONTROL1, 0x08)
        
        
    def get(self):
        second = self.bcd_to_decimal((self.read(PCF8563_SECOND) & 0x7F))
        minute = self.bcd_to_decimal((self.read(PCF8563_MINUTE) & 0x7F))
        hour = self.bcd_to_decimal((self.read(PCF8563_HOUR) & 0x3F))
        day = self.bcd_to_decimal((self.read(PCF8563_DAY) & 0x07))
        date = self.bcd_to_decimal((self.read(PCF8563_DATE) & 0x3F))
        month = self.bcd_to_decimal((self.read(PCF8563_MONTH) & 0x1F))
        year = self.bcd_to_decimal(self.read(PCF8563_YEAR))
        
        return hour, minute, second, day, date, month, year
    
    
    def set(self, hour, minute, second, day, date, month, year):
        self.stop_RTC()
        self.write(PCF8563_SECOND, self.decimal_to_bcd(second))
        self.write(PCF8563_MINUTE, self.decimal_to_bcd(minute))
        self.write(PCF8563_HOUR, self.decimal_to_bcd(hour))
        self.write(PCF8563_DAY, self.decimal_to_bcd(day))
        self.write(PCF8563_DATE, self.decimal_to_bcd(date))
        self.write(PCF8563_MONTH, self.decimal_to_bcd(month))
        self.write(PCF8563_YEAR, self.decimal_to_bcd(year))
        self.start_RTC()
               
        
    def get_alarm(self):
        temp = 0
        alarm_state = 0;
        
        alarm_minute = self.read(PCF8563_ALARM_MINUTE)
        temp = (alarm_minute & 0x80)
        alarm_minute &= 0x7F
        alarm_minute = self.bcd_to_decimal(alarm_minute)
        
        alarm_hour = self.read(PCF8563_ALARM_HOUR)
        alarm_state = ((temp | (alarm_hour & 0x80)) >> 0x07)
        alarm_hour &= 0x3F
        alarm_hour = self.bcd_to_decimal(alarm_hour)
        
        return alarm_hour, alarm_minute
    
    
    def set_alarm(self, alarm_hour, alarm_minute, alarm_state):
        alarm_minute = self.decimal_to_bcd(alarm_minute)
        alarm_hour = self.decimal_to_bcd(alarm_hour)
        
        if(alarm_state == self.alarm_off):
            alarm_minute |= 0x80
            alarm_hour |= 0x80
            
        else:
            alarm_minute &= 0x7F
            alarm_hour &= 0x7F
            self.write(PCF8563_CONTROL2, 0x02)
                       
        self.write(PCF8563_ALARM_HOUR, alarm_hour)
        self.write(PCF8563_ALARM_MINUTE, alarm_minute)

    def check_alarm(self):
        temp = 0
        temp = (self.read(PCF8563_CONTROL2) & 0x08)
        
        if(temp != 0):
            return 1
        
        else:
            return 0
        
        
    def clear_alarm(self):
        temp = 0
        temp = self.read(PCF8563_CONTROL2)
        self.write(PCF8563_CONTROL2, (0xF7 & temp))
