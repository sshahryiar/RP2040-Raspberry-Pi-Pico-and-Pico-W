from micropython import const
from machine import Pin, RTC
from time import sleep_ms, ticks_ms, localtime, gmtime, mktime
from ST7789_2in import TFT2in
from open_weather_map import open_weather_map
import Open_Weather_Map_Credentials
import WiFi_Credentials
from unix_time import unix 
import network
import random
import math
import gc


gc.enable()
gc.collect()
wifi_check_interval = const(120000)
weather_sync_time = const(15)



year = 1970
month = 1
date = 1
hour = 10
count = 0
minute = 10
second = 30
current_tick = 0
previous_tick = 0
first_report = True
connection_status = False
conv_factor_1 = 0.0174532925
conv_factor_2 = 0.104733333
pi_by_2 = 1.570796327
weather_data = [0 for _ in range(0, 23)]


tft = TFT2in()
tft.fill(tft.BLACK)
rtc = RTC()
LED = Pin("LED", Pin.OUT)
ut = unix(6)
owm = open_weather_map(Open_Weather_Map_Credentials.country, Open_Weather_Map_Credentials.city, Open_Weather_Map_Credentials.api_key)


def connect_wifi(ssid, password):
    i = 0
    
    LED.on()
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        gc.collect()
        while (not wlan.isconnected() and (i < 3)):
            LED.on()
            i += 1
            sleep_ms(100)
            LED.off()
            sleep_ms(900)
        
        print('Network connected!')
    
    else:
        print('Already connected to network')
    
    print('IP address:', wlan.ifconfig()[0])
    LED.off()
    return wlan
    
    
def check_connection(wlan):
    global current_tick, previous_tick, ip, connection_status, first_report
    
    current_tick = ticks_ms()
    
    if((current_tick - previous_tick) > wifi_check_interval):
        LED.on()
        gc.collect()
        
        try:
            response = network.WLAN(network.STA_IF).isconnected()
            
            if not response:
                print('Connection lost. Reconnecting...')
                wlan.active(False)
                connection_status = False 
                connect_wifi(WiFi_Credentials.SSID, WiFi_Credentials.password)
            else:
                connection_status = True
                first_report = True 
                
        except Exception as e:
            print('Error checking connection:', e)
            connection_status = False 
            wlan.active(False)
            connect_wifi(WiFi_Credentials.SSID, WiFi_Credentials.password)
    
        LED.off()
        previous_tick = current_tick
        
        
                
def report_time():
    global year, month, date, hour, minute, second
    
    year, month, date, hour, minute, second, ms, tz = localtime()
    
    
def get_weather():
    global first_report, weather_data, connection_status, year, month, date, hour, minute, second, count
    
    
    if((connection_status == True) and ((((minute % weather_sync_time) == 0) and (second == 0)) or (first_report == True))):
        gc.collect()
        try:
            weather_data = owm.fetch_data()
            first_report = False
            
            if(count < weather_data[4]):
                count = weather_data[4]            
                year, month, date, hour, minute, second = ut.unix_to_date_time(count)
                rtc.datetime((year, month, date, 1, hour, minute, second, 0))
            
            print(weather_data)
        except Exception as e:
            print("Unable to download data!", e)
            

def analog_clock(x_pos, y_pos, radius):
    global hour, minute, second
    
    size_1 = (radius >> 1)
    size_2 = ((radius << 1) // 3)
    size_3 = ((radius << 2) // 5)
    
    hour *=  (5 * conv_factor_2)
    minute *= conv_factor_2
    second *= conv_factor_2
    
    tft.ellipse(x_pos, y_pos, (radius + 2), (radius + 2), tft.YELLOW)
    tft.ellipse(x_pos, y_pos, radius, radius, tft.YELLOW)
    tft.ellipse(x_pos, y_pos, 4, 4, tft.BLUE, True)
        
    tft.line(x_pos, y_pos, (x_pos + int(size_1 * math.sin(hour))), int(y_pos - (size_1 * math.cos(hour))), tft.RED)
    tft.line(x_pos, y_pos, (x_pos + int(size_2 * math.sin(minute))), int(y_pos - (size_2 * math.cos(minute))), tft.MAGENTA)
    tft.line(x_pos, y_pos, (x_pos + int(size_3 * math.sin(second))), int(y_pos - (size_3 * math.cos(second))), tft.GREEN)
    

def digital_clock(x_pos, y_pos):
    global year, month, date, hour, minute, second
    
    str_1 = str("%02u" % hour) + ":" + str("%02u" % minute) + ":" + str("%02u" % second)
    str_2 = str("%02u" % date) + "/" + str("%02u" % month) + "/" + str("%04u" % year)
    
    print(str_1 + "  " + str_2)    
    tft.text(str_1, (x_pos + 8), y_pos, tft.WHITE)
    tft.text(str_2, x_pos, (y_pos + 12), tft.WHITE)
    
    
def cloudy(x_pos, y_pos, size, col1, col2):
    tft.ellipse(x_pos, y_pos, size, size, tft.colour_generator(col1, col1, col1), True)
    tft.ellipse((x_pos - 10), (y_pos - 5), size, size, tft.colour_generator(col1, col1, col1), True)
    tft.ellipse((x_pos + 10), (y_pos - 10), size, size, tft.colour_generator(col2, col2, col2), True)
    tft.ellipse((x_pos + 20), y_pos, size, size, tft.colour_generator(col2, col2, col2), True)
    
    
def sunny(x_pos, y_pos, radius):
    global conv_factor
    
    tft.ellipse(x_pos, y_pos, radius, radius, tft.YELLOW, True)
    
    size = (radius << 1)

    for i in range(0, 360, 30):
        tft.line(x_pos, y_pos, (x_pos + int(size * math.sin(i * conv_factor))), int(y_pos - (size * math.cos(i * conv_factor))), tft.YELLOW)


def rain(x_pos, y_pos, size = 20):
    gap = (size >> 2)
    
    for i in range(0, 10):
        xpos = random.randrange(x_pos, (x_pos + size))
        ypos = random.randrange(y_pos, (y_pos + size))
        tft.line(xpos, ypos, (xpos - gap), (ypos - gap), tft.CYAN)
    

def snow(x_pos, y_pos, size = 20):
    radius = (size // 10)
    
    for i in range(0, 10):
        r = random.randrange(1, radius)
        xpos = random.randrange(x_pos, (x_pos + size))
        ypos = random.randrange(y_pos, (y_pos + size))
        tft.ellipse(xpos, ypos, r, r, tft.CYAN, True)
    
    
def lightning(x_pos, y_pos, size = 12):
    gap = (size >> 1)
    xpos = random.randrange(x_pos, (x_pos + (size << 1)))
    ypos = random.randrange(y_pos, (y_pos + size))
    tft.line((xpos + gap), ypos, xpos, (ypos + gap), tft.YELLOW)
    tft.line(xpos, (ypos + gap), (xpos + gap), (ypos + gap), tft.YELLOW)
    tft.line((xpos + gap), (ypos + gap), xpos, (ypos + (gap << 1)), tft.YELLOW)
 

def mist(x_pos, y_pos, size = 40):
    length = (size >> 1)
    gap = (length >> 1)
    
    for i in range(0, gap):
        xpos = random.randrange(x_pos, (x_pos + size), gap)
        ypos = random.randrange(y_pos, (y_pos + size), gap)
        tft.hline(xpos, ypos, length, tft.GREEN)
        
        
def compass(x_pos, y_pos, size, bearing):
    global conv_factor, pi_by_2
    
    size_n = (size >> 3)
    tft.text("N", (x_pos - 4), (y_pos - size - 10), tft.RED)
    tft.ellipse(x_pos, y_pos, size, size, tft.BLUE, False)
    tft.ellipse(x_pos, y_pos, size_n, size_n, tft.BLUE, True)
    
    heading_in_radians = (bearing * conv_factor_1) 
    v1 = int(size * math.cos(heading_in_radians))
    h1 = int(size * math.sin(heading_in_radians))
    tft.line(x_pos, y_pos, (x_pos + h1), (y_pos - v1), tft.GREEN)
    
    v2 = int(size_n * math.cos((heading_in_radians - pi_by_2)))
    h2 = int(size_n * math.sin((heading_in_radians - pi_by_2)))
    tft.line(x_pos, y_pos, (x_pos - h2), (y_pos + v2), tft.CYAN)
    tft.line(x_pos, y_pos, (x_pos + h2), (y_pos - v2), tft.CYAN)
     
    tft.line((x_pos + h1), (y_pos - v1), (x_pos + h2), (y_pos - v2),  tft.CYAN)
    tft.line((x_pos - h1), (y_pos + v1), (x_pos + h2), (y_pos - v2),  tft.CYAN)
    tft.line((x_pos + h1), (y_pos - v1), (x_pos - h2), (y_pos + v2),  tft.CYAN)
    tft.line((x_pos - h1), (y_pos + v1), (x_pos - h2), (y_pos + v2),  tft.CYAN)
    
    
def show_weather_data():
    global weather_data    
    
    tft.text(str(weather_data[0]), 100, 40, tft.WHITE)
    tft.text(str(weather_data[1]), 100, 55, tft.WHITE)
    
    temp_str = "Ta'/C: " + str("%2.1f " %weather_data[9])    
    tft.text(temp_str, 100, 70, tft.WHITE)
    
    temp_str = "R.H/%: " + str("%3.1f " %weather_data[13])
    tft.text(temp_str , 100, 85, tft.WHITE)
        
    temp_str = "P/mbr: " + str("%4.1f " %weather_data[14])
    tft.text(temp_str , 100, 100, tft.WHITE)
   
    temp_str = "W.m/s: " + str("%2.1f " %weather_data[15])
    tft.text(temp_str , 100, 115, tft.WHITE)
    
    temp_str = "W.dir: " + str("%4.1f " %weather_data[16])
    tft.text(temp_str , 100, 130, tft.WHITE)
    
    time = ut.unix_to_date_time(weather_data[6])
    temp_str = "Sunset : " + str("%02u:" %time[3]) + str("%02u:" %time[4]) + str("%02u" %time[5])
    tft.text(temp_str , 100, 145, tft.WHITE)
   
    time = ut.unix_to_date_time(weather_data[5])
    temp_str = "Sunrise: " + str("%02u:" %time[3]) + str("%02u:" %time[4]) + str("%02u" %time[5])
    tft.text(temp_str , 100, 160, tft.WHITE)
          
    compass(285, 144, 24, weather_data[16])
    
    if((weather_data[22] == "01d") or (weather_data[22] == "01n")):
        sunny(260, 55, 20)
        
    elif((weather_data[22] == "02d") or (weather_data[22] == "02n")):
        sunny(260, 54, 20)
        cloudy(270, 60, 15, 165, 165)
        
    elif((weather_data[22] == "03d") or (weather_data[22] == "03n")):
        cloudy(260, 60, 15, 145, 125)
        
    elif((weather_data[22] == "04d") or (weather_data[22] == "04n")):
        sunny(260, 55, 20)
        cloudy(270, 60, 15, 100, 125)
    
    elif((weather_data[22] == "09d") or (weather_data[22] == "09n")):
        cloudy(260, 60, 15, 145, 125)
        rain(266, 70)
        
    elif((weather_data[22] == "10d") or (weather_data[22] == "10n")):
        cloudy(260, 60, 15, 125, 125)
        rain(264, 70)
        
    elif((weather_data[22] == "11d") or (weather_data[22] == "11n")):
        cloudy(260, 60, 15, 145, 125)
        lightning(250, 70)
        
    elif((weather_data[22] == "13d") or (weather_data[22] == "13n")):
        cloudy(260, 60, 15, 145, 125)
        snow(265, 70)
        
    elif((weather_data[22] == "50d") or (weather_data[22] == "50n")):
        cloudy(260, 54, 16, 195, 195)
        mist(240, 60)


gc.collect()
wlan = connect_wifi(WiFi_Credentials.SSID, WiFi_Credentials.password)


while(True):
    gc.collect()
    check_connection(wlan)
    LED.on()
    tft.fill(tft.BLACK)
    tft.text("Raspberry Pi PICO W Open Weather Map", 15, 10, tft.WHITE)    
    report_time() 
    get_weather()
    show_weather_data()
    digital_clock(10, 140)
    analog_clock(50, 80, 40)    
    tft.show()
    sleep_ms(400)
    LED.off()
    sleep_ms(600)
