from micropython import const
from machine import Pin, I2C


DS3231_I2C_Address = const(0x68)            
                                           
DS3231_second_reg = const(0x00)
DS3231_minute_reg = const(0x01)
DS3231_hour_reg = const(0x02)
DS3231_day_reg = const(0x03) 
DS3231_date_reg = const(0x04)
DS3231_month_reg = const(0x05)                            
DS3231_year_reg = const(0x06)                    
DS3231_alarm_1_sec_reg = const(0x07)       
DS3231_alarm_1_min_reg = const(0x08) 
DS3231_alarm_1_hr_reg = const(0x09)           
DS3231_alarm_1_date_reg = const(0x0A)  
DS3231_alarm_2_min_reg = const(0x0B)   
DS3231_alarm_2_hr_reg = const(0x0C) 
DS3231_alarm_2_date_reg = const(0x0D)
DS3231_control_reg = const(0x0E)
DS3231_status_reg = const(0x0F) 
DS3231_ageoffset_reg = const(0x10)
DS3231_temp_MSB_reg = const(0x11)
DS3231_temp_LSB_reg = const(0x12) 


class DS3231():
    def __init__(self, _i2c):
        
        self._24_hour_format = const(0)
        self._12_hour_format = const(1) 
        self.am = const(0)
        self.pm = const(1)
        
        self.i2c = _i2c
        self.i2c_address = DS3231_I2C_Address
        self.init()


    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(self.i2c_address, reg, value)


    def init(self):
        self.write(DS3231_control_reg, 0x00)
        self.write(DS3231_status_reg, 0x08)


    def read(self, reg):
        retval = self.i2c.readfrom_mem(self.i2c_address, reg, 1)    
        return retval[0]


    def bcd_to_decimal(self, value):
        return ((value & 0x0F) + (((value & 0xF0) >> 4) * 10))


    def decimal_to_bcd(self, value):
        return (((value // 10) << 4) & 0xF0) | ((value % 10) & 0x0F)


    def get_temperature(self):
        LB = self.read(DS3231_temp_LSB_reg)
        HB = self.read(DS3231_temp_MSB_reg)
        LB >>= 0x06
        LB &= 0x03
        t = LB
        t *= 0.25
        t += HB
        return t 

    
    def get_time(self, hour_format):
        am_pm_state = 0
        
        second = self.bcd_to_decimal(self.read(DS3231_second_reg))
        minute = self.bcd_to_decimal(self.read(DS3231_minute_reg))

        if(hour_format == self._12_hour_format):
            tmp = self.read(DS3231_hour_reg)
            tmp &= 0x20
            tmp >>= 0x05
            am_pm_state = tmp
            hour = self.bcd_to_decimal((self.read(DS3231_hour_reg) & 0x1F)) 

        else:
            hour = self.bcd_to_decimal((self.read(DS3231_hour_reg) & 0x3F)) 

        return hour, minute, second, am_pm_state


    def get_calendar(self):
        year = self.bcd_to_decimal(self.read(DS3231_year_reg))
        month = self.bcd_to_decimal((self.read(DS3231_month_reg) & 0x1F)) 
        date = self.bcd_to_decimal((self.read(DS3231_date_reg) & 0x3F))
        day = self.bcd_to_decimal((self.read(DS3231_day_reg) & 0x07))

        return day, date, month, year


    def set_time(self, hour, minute, second, am_pm_state, hour_format):
        self.write(DS3231_second_reg, self.decimal_to_bcd(second))
        self.write(DS3231_minute_reg, self.decimal_to_bcd(minute))

        if(hour_format == self._12_hour_format):
            if(am_pm_state == self.pm):
                tmp = 0x60
            
            else:
                tmp = 0x40

            self.write(DS3231_hour_reg, ((tmp | (0x1F & (self.decimal_to_bcd(hour))))))

        else:
            self.write(DS3231_hour_reg, ((0x3F & (self.decimal_to_bcd(hour)))))


    def set_calendar(self, day, date, month, year):
        self.write(DS3231_day_reg, (self.decimal_to_bcd(day)))
        self.write(DS3231_date_reg, (self.decimal_to_bcd(date)))
        self.write(DS3231_month_reg, (self.decimal_to_bcd(month)))
        self.write(DS3231_year_reg, (self.decimal_to_bcd(year)))
