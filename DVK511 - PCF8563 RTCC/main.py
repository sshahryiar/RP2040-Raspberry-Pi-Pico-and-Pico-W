from micropython import const
from machine import Pin, I2C
from utime import sleep_ms
from PCF8563 import PCF8563
from LCD import LCD


LCD_RS = const(22)
LCD_EN = const(10)
LCD_D4 = const(18)
LCD_D5 = const(11)
LCD_D6 = const(12)
LCD_D7 = const(28)


i = 0
index = 0
set_read = 0
hour = 23
minute = 59
second = 45
day = 1
date = 31
month = 12
year = 21


LED = Pin(25, Pin.OUT)
BUZ = Pin(17, Pin.OUT)

BUZ.on()

A_Key = Pin(4, Pin.IN, Pin.PULL_UP)
B_Key = Pin(5, Pin.IN, Pin.PULL_UP)
C_Key = Pin(7, Pin.IN, Pin.PULL_UP)
D_Key = Pin(8, Pin.IN, Pin.PULL_UP)

lcd = LCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7)

i2c =I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
rtc = PCF8563(i2c)

rtc.set(hour, minute, second, day, date, month, year)


def set_parameter(value, value_max, value_min, x_pos, y_pos):
    if(D_Key.value() == False):
        BUZ.toggle()
        LED.toggle()
        sleep_ms(10)
        value += 1
        
    if(value > value_max):
        value = value_min
        
    if(A_Key.value() == False):
        BUZ.toggle()
        LED.toggle()
        sleep_ms(10)
        value -= 1
        
    if(value < value_min):
        value = value_max
        
    lcd.goto_xy(x_pos, y_pos)
    lcd.put_str("  ")
    sleep_ms(10)
    lcd.goto_xy(x_pos, y_pos)
    lcd.put_str(str("%02u" %value))
    sleep_ms(10)
    BUZ.on()
        
    return value


def RTC_run():
    global set_read, i
    
    if(B_Key.value() == False):
        sleep_ms(60)
        if(B_Key.value() == False):
            BUZ.toggle()
            set_read = 1
    
    if(set_read == 1):
        set_time()    
    elif(set_read == 0):
        rtc_read()
        rtc_display()
        
        
def set_time():
    global set_read, index, i, hour, minute, second, day, date, month, year
    
    lcd.goto_xy(0, 0)
    lcd.put_str("SET")   
    
    if(C_Key.value() == False):
        BUZ.toggle()
        sleep_ms(40)
        index += 1
        
    if(index > 6):
        index = 6
        
    if(B_Key.value() == False):
        BUZ.toggle()
        sleep_ms(40)
        index -= 1
        
    if(index < 0):
        index = 0
        
    if(index == 0):
        lcd.goto_xy(0, 1)
        lcd.put_str("HR ")   
        hour = set_parameter(hour, 23, 0, 4, 0)
        
    elif(index == 1):
        lcd.goto_xy(0, 1)
        lcd.put_str("MIN") 
        minute = set_parameter(minute, 59, 0, 7, 0)
        
    elif(index == 2):
        lcd.goto_xy(0, 1)
        lcd.put_str("SEC")
        second = set_parameter(second, 59, 0, 10, 0)
        
    elif(index == 3):
        lcd.goto_xy(0, 1)
        lcd.put_str("DT ") 
        date = set_parameter(date, 31, 1, 4, 1)
        
    elif(index == 4):
        lcd.goto_xy(0, 1)
        lcd.put_str("MTH") 
        month = set_parameter(month, 12, 1, 7, 1)
        
    elif(index == 5):
        lcd.goto_xy(0, 1)
        lcd.put_str("YR ") 
        year = set_parameter(year, 99, 0, 10, 1)
        
    elif(index == 6):
        day = 1
        rtc.set(hour, minute, second, day, date, month, year)
        lcd.goto_xy(0, 0)
        lcd.put_str("   ")
        lcd.goto_xy(0, 1)
        lcd.put_str("   ")
        BUZ.on()
        set_read = 0
        index = 0
    
    sleep_ms(100)
    
    
def rtc_read():
    global hour, minute, second, day, date, month, year
    
    hour, minute, second, day, date, month, year = rtc.get()
    
    
def rtc_display():
    global hour, minute, second, date, month, year
    lcd.goto_xy(4, 0)
    lcd.put_str(str("%02u:" %hour))
    lcd.goto_xy(7, 0)
    lcd.put_str(str("%02u:" %minute))
    lcd.goto_xy(10, 0)
    lcd.put_str(str("%02u" %second))
    lcd.goto_xy(4, 1)
    lcd.put_str(str("%02u/" %date))
    lcd.goto_xy(7, 1)
    lcd.put_str(str("%02u/" %month))
    lcd.goto_xy(10, 1)
    lcd.put_str(str("%02u" %year))
    LED.toggle()
    sleep_ms(990)


while(True):
    RTC_run()
    
    
    
    
