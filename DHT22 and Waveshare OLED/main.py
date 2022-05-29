from machine import Pin
from SH1107 import OLED_13
from utime import sleep_ms
import math
import dht

LED = Pin(25, Pin.OUT)

oled = OLED_13()
RHT = dht.DHT22(Pin(28, Pin.IN))


def map_value(value, x_min, x_max, y_min, y_max):
    return (y_min + (((y_max - y_min)/(x_max - x_min)) * (value - x_min)))


def circle(xc, yc, r, c):
   a = 0
   b = r
   p = (1 - b)
   
   while(a <= b):
       oled.pixel((xc + a), (yc + b), c)
       oled.pixel((xc + b), (yc + a), c)
       oled.pixel((xc - a), (yc + b), c)
       oled.pixel((xc - b), (yc + a), c)
       oled.pixel((xc + b), (yc - a), c)
       oled.pixel((xc + a), (yc - b), c)
       oled.pixel((xc - a), (yc - b), c)
       oled.pixel((xc - b), (yc - a), c)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1  


while True:
    oled.fill(oled.BLACK)
    
    oled.text("Tmp/'C", 6, 1, oled.WHITE)
    oled.text("R.H./%", 73, 1, oled.WHITE)
        
    oled.text("30", 4, 35, oled.WHITE)
    oled.text("50", 25, 30, oled.WHITE)
    oled.text("70", 45, 35, oled.WHITE)

    oled.text("30", 65, 35, oled.WHITE)
    oled.text("50", 85, 30, oled.WHITE)
    oled.text("70", 105, 35, oled.WHITE)
    
    circle(33, 63, 25, oled.WHITE)
    circle(93, 63, 25, oled.WHITE)

    oled.hline(0, 10, 127, oled.WHITE)
    oled.hline(0, 28, 127, oled.WHITE)    
    oled.vline(63, 0, 63, oled.WHITE)
    
    RHT.measure()
    t = RHT.temperature()
    rh = RHT.humidity()
    
    oled.text(str("% 2.1f" % t), 8, 16, oled.WHITE)
    oled.text(str("% 2.1f" % rh), 72, 16, oled.WHITE)

    l1 = map_value(t, 0, 100, -1.571, 1.571)
    l2 = map_value(rh, 0, 100, -1.571, 1.571)
    
    oled.line(33, 63, (33 + int(20 * math.sin(l1))), int(63 - (20 * math.cos(l1))), oled.WHITE)
    oled.line(93, 63, (93 + int(20 * math.sin(l2))), int(63 - (20 * math.cos(l2))), oled.WHITE)

    oled.show()
    
    LED.toggle()
    sleep_ms(100)

    

