from machine import Pin
from utime import sleep_ms, 
from TCS3200 import TCS3200
from ST7789 import TFT114

fc = 0
r = 0
g = 0
b = 0

color_sensor = TCS3200(0, 2, 3, 4, 5)
tft = TFT114()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def contrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value
            
            
def draw_and_write(value, pos, colour):
    bar = map_value(value, 0, 100,  0, 219)
    bar = contrain(bar, 0, 219)
    
    tft.text(str("%3u" %value), 110, (pos + 20), colour)
    
    tft.rect(9, pos, 222, 15, tft.WHITE)
    tft.fill_rect(10, (2 + pos), bar, 11, colour)


while(True):
    r, g, b, fc  = color_sensor.get_color_ratio()

    tft.fill(tft.BLACK)
    tft.text("RP2040 PICO PIO TCS3200", 30, 1, tft.CYAN)
    tft.text("FC/Hz: " + str("%4u" %fc), 85, 25, tft.YELLOW)
    draw_and_write(r, 40, tft.RED)
    draw_and_write(g, 70, tft.GREEN)
    draw_and_write(b, 100, tft.BLUE)
    
    tft.show()
        
    sleep_ms(400)


