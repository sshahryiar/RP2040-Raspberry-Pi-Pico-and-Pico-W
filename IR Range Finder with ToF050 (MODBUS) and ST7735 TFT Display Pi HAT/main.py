from micropython import const
from machine import UART, Pin
from utime import sleep_ms
from ToF050 import ToF050
from ST7735 import TFT_144


LED = Pin(25, Pin.OUT)

tft = TFT_144()

uart = UART(1, baudrate = 115200, tx = Pin(4), rx = Pin(5))
tof = ToF050(uart)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def background():
    tft.text("0", 10, 62, tft.CYAN)
    tft.text("100", 54, 62, tft.CYAN)
    tft.text("200", 100, 62, tft.CYAN)
    
    for i in range(0, 100, 9):
        tft.vline((14 + i), 76, 10, tft.GREEN)
        if(i < 99):
            tft.vline((19+ i), 82, 4, tft.GREEN)
        
    tft.text("ToF050 RP2040",  12, 9, tft.RED)
    tft.text("Range/mm:",  16, 36, tft.WHITE)


while(True):
    r = tof.get_range()
    
    if(r == -1):
        d = tof.max_distance
        r = d

    d = map_value(r, 0, 200, 0, 100)
          
    tft.fill(tft.BLACK)
    background()
    tft.fill_rect(14, 90, d, 16, tft.YELLOW)
    tft.text(str("%03s" %r),  90, 36, tft.WHITE)
    tft.show()
    LED.toggle()
    sleep_ms(100)
