from machine import Pin, UART
from utime import sleep_ms, 
from ST7789 import TFT208
from GY68x import GY68x
import framebuf
import math


uart = UART(1, baudrate = 9600, bits = 8, parity = None, stop = 1, tx = Pin(4), rx = Pin(5))

tft = TFT208()
gy = GY68x(uart)


def circle(xc, yc, r, c):
   a = 0
   b = r
   p = (1 - b)
   
   while(a <= b):
       tft.pixel((xc + a), (yc + b), c)
       tft.pixel((xc + b), (yc + a), c)
       tft.pixel((xc - a), (yc + b), c)
       tft.pixel((xc - b), (yc + a), c)
       tft.pixel((xc + b), (yc - a), c)
       tft.pixel((xc + a), (yc - b), c)
       tft.pixel((xc - a), (yc - b), c)
       tft.pixel((xc - b), (yc - a), c)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1  


def map_value(v, x_min, x_max, y_min, y_max):
    return (y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def constrain(value, min_value, max_value):
    if(value > max_value):
        return max_value
    
    elif(value < min_value):
        return min_value
    
    else:
        return value
    
    
def draw_background_graphics():
    tft.fill(0x1248)
    
    tft.text("RP2040 GY-MCU68x Environment Sensor", 20, 10, tft.WHITE)
    
    circle(40, 100, 2, tft.RED)
    circle(120, 100, 2, tft.GREEN)
    circle(200, 100, 2, tft.YELLOW)
    circle(280, 100, 2, tft.MAGENTA)
    
    for i in range (0, 320, 80):
        circle((40 + i), 100, 34, tft.WHITE)
        circle((40 + i), 100, 36, tft.WHITE)
        
    tft.text("T/deg C", 15, 45, tft.WHITE)
    tft.text("RH/%", 106, 45, tft.WHITE)
    tft.text("P/mbar", 175, 45, tft.WHITE)
    tft.text("Gas/k Ohms", 232, 45, tft.WHITE)
    
    tft.rect(8, 200, 304, 24, tft.WHITE)
    tft.fill_rect(10, 202, 50, 20, tft.BLUE)
    tft.fill_rect(60, 202, 50, 20, tft.CYAN)
    tft.fill_rect(110, 202, 50, 20, tft.GREEN)
    tft.fill_rect(160, 202, 50, 20, tft.YELLOW)
    tft.fill_rect(210, 202, 50, 20, tft.RED)
    tft.fill_rect(260, 202, 50, 20, tft.MAGENTA)
    
    tft.text("<100", 20, 208, tft.BLACK)
    tft.text("100", 75, 208, tft.BLACK)
    tft.text("200", 125, 208, tft.BLACK)
    tft.text("300", 175, 208, tft.BLACK)
    tft.text("400", 225, 208, tft.BLACK)
    tft.text("500", 275, 208, tft.BLACK)
    

def draw_dial(x_pos, y_pos, value, value_min, value_max, colour):
    temp = constrain(value, value_min, value_max)
    line = map_value(temp, value_min, value_max, -2.618, 2.618)    
    tft.line(x_pos, y_pos, (x_pos + int(30 * math.sin(line))), int(y_pos - (30 * math.cos(line))), colour)
    
    
def draw_pointer(value, value_min, value_max):
    temp = constrain(value, value_min, value_max)
    temp = int(map_value(temp, value_min, value_max, 10, 310))
    tft.line(temp, 194, (temp - 4), 190, tft.WHITE)
    tft.line(temp, 194, (temp + 4), 190, tft.WHITE)
    tft.line((temp - 4), 190, (temp + 4), 190, tft.WHITE)
    


while(True):
    draw_background_graphics()
    
    t, rh, p, iaq, gas, alt = gy.get_data()
    
    tft.text(str("%2.1f" %t), 25, 145, tft.WHITE)
    tft.text(str("%2.1f" %rh), 105, 145, tft.WHITE)
    tft.text(str("%3.1f" %p), 185, 145, tft.WHITE)
    tft.text(str("%3.1f" %gas), 270, 145, tft.WHITE)
    tft.text(("IAQ: " + str("%3.1f" %iaq)), 130, 170, tft.WHITE)
    
    draw_dial(40, 100, t, gy.t_min, gy.t_max, tft.RED)
    draw_dial(120, 100, rh, gy.rh_min, gy.rh_max, tft.GREEN)
    draw_dial(200, 100, p, gy.p_min, gy.p_max, tft.YELLOW)
    draw_dial(280, 100, gas, gy.gas_min, gy.gas_max, tft.MAGENTA)
    draw_pointer(iaq, gy.iaq_min, gy.iaq_max)
    
    
    tft.show()
        
    sleep_ms(100)
