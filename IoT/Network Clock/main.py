from machine import Pin
from utime import sleep_ms
from WiFi import wifi
from SH1107 import OLED_13
import WiFi_Credentials
import time
import math
import ujson


sync_hour = const(3)

i = 0
time_fetch_flag = False
time_sync_status = False
connection_status = False

hour = 10
minute = 10
second = 30
date = 1
month = 1
year = 1970
weekday = 0
yearday = 1

esp = wifi()
oled = OLED_13()
LED = Pin(25, Pin.OUT)


def circle(xc, yc, r, f, colour):
       a = 0
       b = r
       p = (1 - b)
       
       while(a <= b):
           if(f == True):
               oled.line((xc - a), (yc + b), (xc + a), (yc + b), colour)
               oled.line((xc - a), (yc - b), (xc + a), (yc - b), colour)
               oled.line((xc - b), (yc + a), (xc + b), (yc + a), colour)
               oled.line((xc - b), (yc - a), (xc + b), (yc - a), colour)
               
           else:
               oled.pixel((xc + a), (yc + b), colour)
               oled.pixel((xc + b), (yc + a), colour)
               oled.pixel((xc - a), (yc + b), colour)
               oled.pixel((xc - b), (yc + a), colour)
               oled.pixel((xc + b), (yc - a), colour)
               oled.pixel((xc + a), (yc - b), colour)
               oled.pixel((xc - a), (yc - b), colour)
               oled.pixel((xc - b), (yc - a), colour)
            
           if(p < 0):
               p += (3 + (2 * a))
               a += 1
            
           else:
               p += (5 + (2 * (a  - b)))
               a += 1
               b -= 1


def background():
    oled.fill(oled.BLACK)
    oled.text("PICO WiFi Clock", 6, 0, oled.WHITE)
    circle(26, 36, 26, False, oled.WHITE)
    circle(26, 36, 24, False, oled.WHITE)
    circle(26, 36, 1, True, oled.WHITE)
    


def analogue_clock():
    oled.line(26, 36, int(26 + (9 * math.sin((hour + (minute / 60)) * 5 * 0.105))), int(36 - (9 * math.cos((hour + (minute / 60)) * 5 * 0.105))), oled.WHITE)
    oled.line(26, 36, (26 + int(16 * math.sin(minute * 0.105))), int(36 - (16 * math.cos(minute * 0.105))), oled.WHITE)
    oled.line(26, 36, (26 + int(21 * math.sin(second * 0.105))), int(36 - (21 * math.cos(second * 0.105))), oled.WHITE)
    
    
def digital_clock():
    oled.text(str("%02u" % hour), 68, 15, oled.WHITE)
    oled.text(":", 82, 15, oled.WHITE)
    oled.text(str("%02u" % minute), 89, 15, oled.WHITE)
    oled.text(":", 103, 15, oled.WHITE)
    oled.text(str("%02u" % second), 110, 15, oled.WHITE)
    
    oled.text(str("%02u" % date), 54, 30, oled.WHITE)
    oled.text(".", 68, 30, oled.WHITE)
    oled.text(str("%02u" % month), 75, 30, oled.WHITE)
    oled.text(".", 89, 30, oled.WHITE)
    oled.text(str("%04u" % year), 96, 30, oled.WHITE)
    
    print("Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second))
    print("Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) + "\r\n")


oled.fill(oled.BLACK)
oled.show()


while(True):

    if(((minute % 30) == 0) and (second == 30)):
        if(esp.get_connection_status() == False):
            esp.set_mode(esp.STA_AP_mode)
            esp.set_SSID_password(WiFi_Credentials.SSID, WiFi_Credentials.password, True)
            print(esp.get_IP())
            minute = 10
            second = 30
            connection_status = False
        else:
            connection_status = True
        
    if(connection_status == True):
        if(time_sync_status == False):            
            if(second == 30):
                time_fetch_flag = True
                time_sync_status = True
        else:
            
            if(((hour % sync_hour) == 0) and (minute == 0) and (second == 0)):
                time_fetch_flag = True
                
        if(time_fetch_flag == True):
            oled.text("Sync:", 60, 50, oled.WHITE)
            j = esp.http_get("worldtimeapi.org/api/timezone/Asia/Dhaka")
            msg_string = esp.requested_data(esp.rxd)

            try:
                msg = ujson.loads(msg_string)
                i = int(msg["unixtime"])
                print(i)
                print("\r\n")
                time.gmtime(i)
                year, month, date, hour, minute, second, weekday, yearday = time.localtime() 
                oled.text("OK.", 96, 50, oled.WHITE)
                
            except:
                print("Sync Error!")
                oled.text("!", 96, 50, oled.WHITE)
                
            time_fetch_flag = False
            
    background()
    analogue_clock()
    digital_clock()
    year, month, date, hour, minute, second, weekday, yearday = time.localtime()
    oled.show()
    LED.toggle()
    sleep_ms(900)
