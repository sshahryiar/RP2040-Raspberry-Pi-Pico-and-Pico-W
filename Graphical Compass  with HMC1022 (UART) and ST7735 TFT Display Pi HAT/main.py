from micropython import const
from machine import UART, Pin
from utime import sleep_ms
from HMC1022 import HMC1022
from ST7735 import TFT_144
import math


scale_factor_1 = const(42)
scale_factor_2 = const(6)


conv_factor = 0.0174532925
pi_by_2 = 1.570796327


LED = Pin(25, Pin.OUT)

tft = TFT_144()

uart = UART(1, baudrate = 9600, tx = Pin(4), rx = Pin(5))
compass = HMC1022(uart, 18)


def circle(xc, yc, r, f, colour):
    a = 0
    b = r
    p = (1 - b)

    while(a <= b):
       if(f == True):
           tft.line((xc - a), (yc + b), (xc + a), (yc + b), colour)
           tft.line((xc - a), (yc - b), (xc + a), (yc - b), colour)
           tft.line((xc - b), (yc + a), (xc + b), (yc + a), colour)
           tft.line((xc - b), (yc - a), (xc + b), (yc - a), colour)
           
       else:
           tft.pixel((xc + a), (yc + b), colour)
           tft.pixel((xc + b), (yc + a), colour)
           tft.pixel((xc - a), (yc + b), colour)
           tft.pixel((xc - b), (yc + a), colour)
           tft.pixel((xc + b), (yc - a), colour)
           tft.pixel((xc + a), (yc - b), colour)
           tft.pixel((xc - a), (yc - b), colour)
           tft.pixel((xc - b), (yc - a), colour)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1
           
           
def draw_background():
    circle(63, 60, 48, False, tft.RED)
    circle(63, 60, 46, False, tft.RED)
    circle(63, 60, 4, True, tft.BLUE)
    
    tft.text("N", 60, 1, tft.GREEN)
    tft.text(" N", 80, 115, tft.WHITE)
    

while(True):
    tft.fill(tft.BLACK)
    
    heading_in_degrees = compass.get_heading()
    tft.text(str("%03.1f" %heading_in_degrees), 40, 115, tft.WHITE)
    
    heading_in_radians = (heading_in_degrees * conv_factor) 
    v1 = int(scale_factor_1 * math.cos(heading_in_radians))
    h1 = int(scale_factor_1 * math.sin(heading_in_radians))
    tft.line(63, 60, (63 + h1), (60 - v1), tft.YELLOW)
    
    v2 = int(scale_factor_2 * math.cos((heading_in_radians - pi_by_2)))
    h2 = int(scale_factor_2 * math.sin((heading_in_radians - pi_by_2)))
    tft.line(63, 60, (63 - h2), (60 + v2), tft.CYAN)
    tft.line(63, 60, (63 + h2), (60 - v2), tft.CYAN)
     
    tft.line((63 + h1), (60 - v1), (63 + h2), (60 - v2),  tft.CYAN)
    tft.line((63 - h1), (60 + v1), (63 + h2), (60 - v2),  tft.CYAN)
    tft.line((63 + h1), (60 - v1), (63 - h2), (60 + v2),  tft.CYAN)
    tft.line((63 - h1), (60 + v1), (63 - h2), (60 + v2),  tft.CYAN)
    
    draw_background()
    tft.show()
    
    LED.toggle()
    sleep_ms(600)
