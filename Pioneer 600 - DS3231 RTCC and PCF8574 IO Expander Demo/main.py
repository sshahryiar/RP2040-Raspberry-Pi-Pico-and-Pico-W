from machine import Pin, I2C
from SSD1306_I2C import OLED1306
from DS3231 import DS3231
from PCF8574 import PCF8574
from utime import sleep_ms


i = 0
j = 0
kbd = 0
set_read = 0
index = 0
day = 0
date = 31
month = 12
year = 21
hour = 23
minute = 59
second = 45
am_pm_state = 1


LED = Pin(25, Pin.OUT)
i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 100000)
oled = OLED1306(i2c)
rtc = DS3231(i2c)
io = PCF8574(i2c)

rtc.set_calendar(day, date, month, year)
rtc.set_time(hour, minute, second, am_pm_state, rtc._24_hour_format)


def read_keys():
    global kbd
    
    kbd = io.port_read(0x0F) & 0x0F


def set_parameter(value, value_max, value_min):
    global kbd
    
    if(kbd == 0x0B):
        LED.toggle()
        io.pin_write(7, 0)
        sleep_ms(30)
        io.pin_write(7, 1)
        value += 1
        
    if(value > value_max):
        value = value_min
        
    if(kbd == 0x0D):
        LED.toggle()
        io.pin_write(7, 0)
        sleep_ms(30)
        io.pin_write(7, 1)
        value -= 1
        
    if(value < value_min):
        value = value_max
    
    
    return value


def select_mode():
    global set_read, i, j
    
    if(kbd == 0x0B):
        sleep_ms(60)
        if(kbd == 0x0B):
            set_read = 1
    
    if(set_read == 1):
        set_time()    
    elif(set_read == 0):
        get_time()


def rtc_display():
    global hour, minute, second, date, month, year
    
    oled.text("Time & Date", 22, 6, oled.WHITE)
    oled.text(str("%02u" % hour), 38, 17, oled.WHITE)
    oled.text(":", 52, 17, oled.WHITE)
    oled.text(str("%02u" % minute), 59, 17, oled.WHITE)
    oled.text(":", 73, 17, oled.WHITE)
    oled.text(str("%02u" % second), 80, 17, oled.WHITE)
    oled.text(str("%02u" % date), 38, 29, oled.WHITE)
    oled.text(".", 52, 29, oled.WHITE)
    oled.text(str("%02u" % month), 59, 29, oled.WHITE)
    oled.text(".", 73, 29, oled.WHITE)
    oled.text(str("%02u" % year), 80, 29, oled.WHITE)
    
    t = rtc.get_temperature()
    oled.text("Temperature", 22, 46, oled.WHITE)
    oled.text(str("%2.2f" % t), 49, 57, oled.WHITE)
    oled.show()


def get_time():
    global hour, minute, second, am_pm_state, day, date, month, year
    
    day, date, month, year = rtc.get_calendar()
    hour, minute, second, am_pm_state = rtc.get_time(rtc._24_hour_format)
    
    io.pin_toggle(4)
    sleep_ms(500)
    
    
def set_time():
    global hour, minute, second, am_pm_state, day, date, month, year, index, set_read, kbd
    
    if(kbd == 0x0E):
        sleep_ms(40)
        index += 1
        
    if(index > 6):
        index = 6
        
    if(kbd == 0x07):
        sleep_ms(40)
        index -= 1
        
    if(index < 0):
        index = 0
    
    if(index == 0):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Hr", 0, 30, oled.WHITE)
        hour = set_parameter(hour, 23, 0)
    elif(index == 1):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Min", 0, 30, oled.WHITE)
        minute = set_parameter(minute, 59, 0)
    elif(index == 2):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Sec", 0, 30, oled.WHITE)
        second = set_parameter(second, 59, 0)
    elif(index == 3):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Day", 0, 30, oled.WHITE)
        date = set_parameter(date, 31, 1)
    elif(index == 4):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Mth", 0, 30, oled.WHITE)
        month = set_parameter(month, 12, 1)
    elif(index == 5):
        oled.text("Set", 0, 20, oled.WHITE)
        oled.text("Yr", 0, 30, oled.WHITE)
        year = set_parameter(year, 99, 0)
    elif(index == 6):
        rtc.set_calendar(day, date, month, year)
        rtc.set_time(hour, minute, second, am_pm_state, rtc._24_hour_format)
        set_read = 0
        index = 0
        
    io.pin_toggle(4)
    sleep_ms(40)
    


while True:
    oled.fill(oled.BLACK)
    read_keys()
    select_mode()
    rtc_display()  
    

