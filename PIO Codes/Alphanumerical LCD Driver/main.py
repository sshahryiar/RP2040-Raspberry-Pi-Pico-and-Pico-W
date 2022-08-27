from machine import Pin
from utime import sleep_ms, 
from LCD_2x16 import LCD


i = -11.0


lcd = LCD(0)


lcd.clear_home()
lcd.goto_xy(1, 0)
lcd.put_str("RP2040 PIO LCD")


while(True):
    lcd.goto_xy(6, 1)
    lcd.put_str(str("%2.1f " % i))
    i += 0.1
    sleep_ms(100)
    
    if(i >= 100):
        i = -11.0
    

