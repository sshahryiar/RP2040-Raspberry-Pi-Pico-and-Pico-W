from ST7735 import TFT18
from machine import Pin
from utime import sleep_ms
from onewire import OneWire
from ds18x20 import DS18X20
import array as array


LED = Pin(25, Pin.OUT)

lcd = TFT18()

ow = OneWire(Pin(28))
ds = DS18X20(ow)
roms = ds.scan()


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def circle(xc, yc, r, f, colour):
    a = 0
    b = r
    p = (1 - b)

    while(a <= b):
       if(f == True):
           lcd.line((xc - a), (yc + b), (xc + a), (yc + b), colour)
           lcd.line((xc - a), (yc - b), (xc + a), (yc - b), colour)
           lcd.line((xc - b), (yc + a), (xc + b), (yc + a), colour)
           lcd.line((xc - b), (yc - a), (xc + b), (yc - a), colour)
           
       else:
           lcd.pixel((xc + a), (yc + b), colour)
           lcd.pixel((xc + b), (yc + a), colour)
           lcd.pixel((xc - a), (yc + b), colour)
           lcd.pixel((xc - b), (yc + a), colour)
           lcd.pixel((xc + b), (yc - a), colour)
           lcd.pixel((xc + a), (yc - b), colour)
           lcd.pixel((xc - a), (yc - b), colour)
           lcd.pixel((xc - b), (yc - a), colour)
        
       if(p < 0):
           p += (3 + (2 * a))
           a += 1
        
       else:
           p += (5 + (2 * (a  - b)))
           a += 1
           b -= 1
           
           
def draw_background():
    lcd.text("Tmp 1", 15, 2, lcd.MAGENTA)
    lcd.text("Tmp 2", 72, 2, lcd.MAGENTA)
    
    circle(33, 145, 9 , False, lcd.WHITE)
    lcd.line(31, 139, 35, 139, lcd.BLACK)
    lcd.line(30, 137, 30, 34, lcd.WHITE)
    lcd.line(36, 137, 36, 34, lcd.WHITE)
    lcd.line(31, 33, 35, 33, lcd.WHITE)
    lcd.line(32, 33, 34, 33, lcd.BLACK)
    lcd.line(32, 32, 34, 32, lcd.WHITE)
    circle(33, 145, 7, True, lcd.RED)
    lcd.fill_rect(33, 137, 2, 1, lcd.RED)
    
    circle(93, 145, 9 , False, lcd.WHITE)
    lcd.line(91, 139, 95, 139, lcd.BLACK)
    lcd.line(90, 137, 90, 34, lcd.WHITE)
    lcd.line(96, 137, 96, 34, lcd.WHITE)
    lcd.line(91, 33, 95, 33, lcd.WHITE)
    lcd.line(92, 33, 94, 33, lcd.BLACK)
    lcd.line(92, 32, 94, 32, lcd.WHITE)
    circle(93, 145, 7, True, lcd.RED)
    lcd.fill_rect(93, 137, 2, 1, lcd.RED)
    
    for i in range (0, 100, 10):
        lcd.line(41, (41 + i), 43, (41 + i), lcd.YELLOW)
        lcd.line(83, (41 + i), 85, (41 + i), lcd.YELLOW)
        
    for i in range (0, 110, 10):
        lcd.line(41, (36 + i), 45, (36 + i), lcd.YELLOW)
        lcd.line(81, (36 + i), 85, (36 + i), lcd.YELLOW)
        
        lcd.text(str("%s" % (100 - int(1.5 * i))), 52, (36 + i), lcd.CYAN)
        

def temp_bar(x_pos, y_pos, bar):
    for i in range (0, 3):
        lcd.line((x_pos + i), y_pos, (x_pos + i), bar, lcd.RED)
    
           
while True:
    i = 0
    LED.toggle()
    tmp = array.array('f', [0, 0])
    lcd.fill(lcd.BLACK)
    draw_background()
    
    ds.convert_temp()
    sleep_ms(750)

    for rom in roms:
        j = int.from_bytes(rom, "big")
        tmp[i] = ds.read_temp(rom)
        print("ROM Code: " + str("%08x" % j) + " - Temp/Deg. C: "  + str("%2.1f" % tmp[i]))       
        i += 1
    
    lcd.text(str("%2.1f" % tmp[0]), 18, 16, lcd.GREEN)
    lcd.text(str("%2.1f" % tmp[1]), 75, 16, lcd.GREEN)
    
    bar1 = map_value(tmp[0], -50, 100,  137, 36)
    bar2 = map_value(tmp[1], -50, 100,  137, 36)
    
    temp_bar(32, 137, bar1)
    temp_bar(92, 137, bar2)
    
    lcd.display()           

