from machine import Pin
from utime import sleep_ms
from WiFi import wifi
from ST7735 import TFT18
import Weather_Stack_Credential
import WiFi_Credentials
import time


sync_hour = const(1)

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

w_msg1 = "--"
w_msg2 = "--"
w_msg3 = "--"
w_msg4 = "--"
w_msg5 = "--"
w_msg6 = "--"
w_msg7 = "--"
w_msg8 = "--"


lat = "23.88"
lon = "90.39"
url = "api.weatherstack.com/current?access_key=" + Weather_Stack_Credential.api_key + "&query=Dhaka"


esp = wifi()
tft = TFT18()
LED = Pin(25, Pin.OUT)


def background():
    tft.fill(tft.BLACK)
    tft.text("RP2040 Weather Stack", 0, 3, tft.WHITE)
    
    tft.text("Temperature/'C:", 0, 20, tft.WHITE)
    tft.text("Pressure /mbar:", 0, 32, tft.WHITE)
    tft.text("R. Humidity/ %:", 0, 44, tft.WHITE)
    tft.text("Wind Speed/m/s:", 0, 56, tft.WHITE)
    tft.text("Wind Dir. / 'N:", 0, 68, tft.WHITE)
    tft.text("uV Index      :", 0, 80, tft.WHITE)
    tft.text("Visibility./km:", 0, 92, tft.WHITE)
    tft.text("Cloud Cover./%:", 0, 104, tft.WHITE)
    tft.text("Lat:", 0, 116, tft.WHITE)
    tft.text("Lon:", 80, 116, tft.WHITE)
    tft.text(lat, 36, 116, tft.WHITE)
    tft.text(lon, 116, 116, tft.WHITE)


tft.fill(tft.BLACK)
tft.display()


while(True):
    background()

    if(((minute % 10) == 0) and (second == 30)):
        if(esp.get_connection_status() == False):
            esp.set_mode(esp.STA_AP_mode)
            esp.set_SSID_password(WiFi_Credentials.SSID, WiFi_Credentials.password, True)
            print(esp.get_IP())
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
            j = esp.http_get("worldtimeapi.org/api/timezone/Asia/Dhaka")

            try:
                msg = esp.search('unixtime', ',', 1)
                i = int(msg)
                print(i)
                time.gmtime(i)
                year, month, date, hour, minute, second, weekday, yearday = time.localtime() 
                time_fetch_flag = False
                
            except:
                print("Error Syncing Time! Retrying....")
                time_sync_status = False
            
            esp.close_connection()
            
            j = esp.http_get(url)
            
            try:
                w_msg1 = esp.search('temperature', ',', 1)
                w_msg2 = esp.search("pressure", ",", 1)
                w_msg3 = esp.search("humidity", ",", 1)                
                w_msg4 = esp.search('wind_speed', ',', 1)
                w_msg5 = esp.search("wind_degree", ",", 1)
                w_msg6 = esp.search("uv_index", ",", 1)
                w_msg7 = esp.search("visibility", ",", 1)
                w_msg8 = esp.search("cloudcover", ",", 1)
                print("Successfully Fetched Weather Data.")
                
            except:
                w_msg1 = " "
                w_msg2 = " "
                w_msg3 = " "
                w_msg4 = " "
                w_msg5 = " "
                w_msg6 = " "
                w_msg7 = " "
                w_msg8 = " "
                print("Error Fetching Weather Data!")
                
            esp.close_connection()
  
    year, month, date, hour, minute, second, weekday, yearday = time.localtime()
    
    tft.text(w_msg1, 124, 20, tft.WHITE)
    tft.text(w_msg2, 124, 32, tft.WHITE)
    tft.text(w_msg3, 124, 44, tft.WHITE)
    tft.text(w_msg4, 124, 56, tft.WHITE)
    tft.text(w_msg5, 124, 68, tft.WHITE)
    tft.text(w_msg6, 124, 80, tft.WHITE)
    tft.text(w_msg7, 124, 92, tft.WHITE)
    tft.text(w_msg8, 124, 104, tft.WHITE)
    
    tft.display()
    
    print("Time: " + str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second))
    print("Date: " + str("%02u" % date) + "." + str("%02u" % month) + "." + str("%04u" % year) + "\r\n")
    LED.toggle()
    sleep_ms(900)

