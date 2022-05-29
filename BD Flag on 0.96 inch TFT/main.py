from ST7735 import TFT096
import utime
import random
import math


lcd = TFT096()


def circle(x,y,r,c):
    lcd.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        lcd.hline(x-a,y+i,a*2,c) # Lower half
        lcd.hline(x-a,y-i,a*2,c) # Upper half
        lcd.display()
        
def ring(x,y,r,c):
    lcd.pixel(x-r,y,c)
    lcd.pixel(x+r,y,c)
    lcd.pixel(x,y-r,c)
    lcd.pixel(x,y+r,c)
    lcd.display()
    utime.sleep(0.1)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i))
        lcd.pixel(x-a,y-i,c)
        lcd.pixel(x+a,y-i,c)
        lcd.pixel(x-a,y+i,c)
        lcd.pixel(x+a,y+i,c)
        lcd.pixel(x-i,y-a,c)
        lcd.pixel(x+i,y-a,c)
        lcd.pixel(x-i,y+a,c)
        lcd.pixel(x+i,y+a,c)
        lcd.display()

lcd.fill(lcd.GREEN)
circle(80, 39, 20, lcd.RED)


