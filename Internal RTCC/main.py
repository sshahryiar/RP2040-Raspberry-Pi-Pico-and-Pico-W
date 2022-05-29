from machine import Pin, RTC
from ST7735 import TFT096
from utime import sleep_ms 
import math


UP_key = Pin(2, Pin.IN, Pin.PULL_UP)
DOWN_key = Pin(18, Pin.IN, Pin.PULL_UP)
LEFT_key = Pin(16, Pin.IN, Pin.PULL_UP)
RIGHT_key = Pin(20, Pin.IN, Pin.PULL_UP)
CENTER_key = Pin(3, Pin.IN, Pin.PULL_UP)
A_key = Pin(15, Pin.IN, Pin.PULL_UP)
B_key = Pin(17, Pin.IN, Pin.PULL_UP)

LED = Pin(25, Pin.OUT)

lcd = TFT096()
rtc = RTC()


i = 0
j = 0
index = 0
set_read = 0
year = 2021
month = 12
date = 31
day = 0
hour = 23
minute = 59
second = 45
time_zone = +6

border_colour = (lcd.RED, lcd.BLUE, lcd.GREEN, lcd.MAGENTA, lcd.CYAN, lcd.YELLOW)
text_colour = (lcd.CYAN, lcd.YELLOW, lcd.RED, lcd.BLUE, lcd.GREEN, lcd.MAGENTA)
hr_hand_colour =  (lcd.BLUE, lcd.GREEN, lcd.MAGENTA, lcd.CYAN, lcd.YELLOW, lcd.RED)
min_hand_colour =  (lcd.GREEN, lcd.MAGENTA, lcd.CYAN, lcd.YELLOW, lcd.RED, lcd.BLUE,)
sec_hand_colour =  (lcd.MAGENTA, lcd.CYAN, lcd.YELLOW, lcd.RED, lcd.BLUE, lcd.GREEN, )


rtc_val = (year, month, date, day, hour, minute, second, time_zone)
rtc.datetime(rtc_val)


def set_parameter(value, value_max, value_min):
    if(UP_key.value() == False):
        LED.toggle()
        sleep_ms(30)
        value += 1
        
    if(value > value_max):
        value = value_min
        
    if(DOWN_key.value() == False):
        LED.toggle()
        sleep_ms(30)
        value -= 1
        
    if(value < value_min):
        value = value_max
        
    return value 


def select_mode():
    global set_read, i, j
    
    if(A_key.value() == False):
        sleep_ms(60)
        if(A_key.value() == False):
            set_read = 1
    
    if(set_read == 1):
        set_time()    
    elif(set_read == 0):
        read_time()
        
    if(B_key.value() == False):
        sleep_ms(60)
        if(B_key.value() == False):
            i += 1
            
    if(i >= 6 ):
        i = 0
        
    if(CENTER_key.value() == False):
        sleep_ms(60)
        if(CENTER_key.value() == False):
            j += 1
            
    if(j >= 6 ):
        j = 0


def read_time():
    global year, month, date, hour, minute, second, rtc_val
    
    rtc_val = rtc.datetime()
    
    year = rtc_val[0]
    month = rtc_val[1]
    date = rtc_val[2]
    hour = rtc_val[4]
    minute = rtc_val[5]
    second = rtc_val[6]
    
    LED.toggle()
    sleep_ms(990)
    
    
def set_time():
    global year, month, date, hour, minute, second, rtc_val, index, set_read
   
    print(index)
    print("\r\n")
   
    if(RIGHT_key.value() == False):
        sleep_ms(40)
        index += 1
        
    if(index > 6):
        index = 6
        
    if(LEFT_key.value() == False):
        sleep_ms(40)
        index -= 1
        
    if(index < 0):
        index = 0
    
    if(index == 0):
        lcd.text("Set Hour", 86, 72, lcd.MAGENTA)
        hour = set_parameter(hour, 23, 0)
    elif(index == 1):
        lcd.text("Set Min", 86, 72, lcd.MAGENTA)
        minute = set_parameter(minute, 59, 0)
    elif(index == 2):
        lcd.text("Set Sec", 86, 72, lcd.MAGENTA)
        second = set_parameter(second, 59, 0)
    elif(index == 3):
        lcd.text("Set Date", 86, 72, lcd.MAGENTA)
        date = set_parameter(date, 31, 1)
    elif(index == 4):
        lcd.text("Set Month", 86, 72, lcd.MAGENTA)
        month = set_parameter(month, 12, 1)
    elif(index == 5):
        lcd.text("Set Year", 86, 72, lcd.MAGENTA)
        year = set_parameter(year, 2099, 1970)
    elif(index == 6):
        rtc_val = (year, month, date, day, hour, minute, second, time_zone)
        rtc.datetime(rtc_val)
        lcd.text("            ", 86, 72, lcd.BLACK)
        set_read = 0
        index = 0
    
    sleep_ms(100)


def analog_clock():
    global border_colour, hr_hand_colour, min_hand_colour, sec_hand_colour, text_colour, i, j
    
    lcd.fill(lcd.BLACK)
    
    lcd.rect(1, 1, 77, 77, border_colour[i])
    lcd.rect(3, 3, 73, 73, border_colour[i])
    
    lcd.text("RP2040", 96, 10, text_colour[i])
    lcd.text("RTC", 108, 20, text_colour[i])
    
    lcd.line(39, 39, (39 + int(18 * math.sin(hour * 5 * 0.105))), int(39 - (18 * math.cos(hour * 5 * 0.105))), hr_hand_colour[j])
    lcd.line(39, 39, (39 + int(24 * math.sin(minute * 0.105))), int(39 - (24 * math.cos(minute * 0.105))), min_hand_colour[j])
    lcd.line(39, 39, (39 + int(30 * math.sin(second * 0.105))), int(39 - (30 * math.cos(second * 0.105))), sec_hand_colour[j])
    
    
def digital_clock():    
    lcd.text(str("%02u" % hour), 94, 40, text_colour[i])
    lcd.text(":", 108, 40, text_colour[i])
    lcd.text(str("%02u" % minute), 115, 40, text_colour[i])
    lcd.text(":", 128, 40, text_colour[i])
    lcd.text(str("%02u" % second), 135, 40, text_colour[i])
    
    lcd.text(str("%02u" % date), 86, 55, text_colour[i])
    lcd.text("/", 100, 55, text_colour[i])
    lcd.text(str("%02u" % month), 107, 55, text_colour[i])
    lcd.text("/", 120, 55, text_colour[i])
    lcd.text(str("%04u" % year), 127, 55, text_colour[i])
    
    
def serial_clock():
    print("Current Time:")
    print(str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second))
    print(str("%02u" % date) + "/" + str("%02u" % month) + ":" + str("%04u" % year) + "\r\n")


while True:
    analog_clock()
    digital_clock()    
    serial_clock()
    select_mode()
    lcd.display()
    




