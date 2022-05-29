from micropython import const
from machine import UART, Pin
from utime import sleep_ms
from ST7735 import TFT096
from RCWL1605 import RCWL1605


tft = TFT096()

uart = UART(1, baudrate = 9600, bits = 8, parity = None, stop = 1, tx = Pin(4), rx = Pin(5))
sonar = RCWL1605(uart)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def background():
    for i in range(0, 150, 9):
        tft.vline((4 + i), 56, 10, tft.GREEN)
        if(i < 144):
            tft.vline((9+ i), 62, 4, tft.GREEN)
        
    tft.text("RCWL1605 RP2040",  20, 4, tft.RED)
    tft.text("Range/mm:", 30, 32, tft.WHITE)


while(True):
    r = sonar.get_distance()
    
    if((r == -1) or (r > 5500)):
        r = 5500
    
    d = map_value(r, 0, 5500, 0, 150)
         
    tft.fill(tft.BLACK)
    background()
    tft.fill_rect(4, 74, d, 4, tft.BLUE)
    tft.text(str("%04s" %r),  100, 32, tft.WHITE)
    tft.display()
    sleep_ms(600)

