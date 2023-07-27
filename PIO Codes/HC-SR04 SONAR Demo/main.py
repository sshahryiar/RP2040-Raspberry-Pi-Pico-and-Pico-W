from machine import Pin
from utime import sleep_ms
from rp2 import asm_pio, StateMachine, PIO
from SONAR import SONAR
from ST7789 import TFT114


bar = 0
distance = 0

sonar = SONAR(15, 14)
tft = TFT114()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value

    else:
        return value
    


def write_text(text, x, y, size, color):
        background = tft.pixel(x, y)
        info = []
        
        tft.text(text, x, y, color)
        for i in range(x, x + (8 * len(text))):
            for j in range(y, y + 8):
                px_color = tft.pixel(i, j)
                info.append((i, j, px_color)) if px_color == color else None
        
        tft.text(text, x, y, background)
       
        for px_info in info:
            tft.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 


while(True):
    
    distance = sonar.get_reading_in_cm()
    distance = constrain(distance, 0, 500)
    bar = map_value(distance, 0, 500,  0, 219)
    bar = constrain(bar, 0, 219)
    tft.fill(tft.BLACK)
    
    write_text("HC-SR04 PIO", 25, 4, 2, tft.WHITE)
    write_text("D/cm: " + str("%3u" %distance), 6, 45, 3, tft.YELLOW)
    tft.rect(9, 90, 222, 15, tft.RED)
    tft.fill_rect(10, 92, bar, 13, tft.GREEN)
    
    for i in range(0, 230, 20):
        tft.vline((10 + i), 112, 10, tft.BLUE)
        tft.vline((20 + i), 112, 5, tft.MAGENTA)
    
    tft.show()
    
    sleep_ms(600)

