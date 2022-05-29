from RGB_LCD_1602 import RGB1602
from utime import sleep_ms


i = -20.0

lcd = RGB1602(2, 16)


lcd.goto_xy(1, 0)
lcd.put_str("WShare RGB LCD")

while True:
    lcd.goto_xy(7, 1)
    lcd.put_str(str("%2.1f " % i))
    i += 0.1
    

    if (-20 < i <= -10):
        lcd.set_RGB(127, 127, 127)
        
    elif (-10 < i <= 0):
        lcd.set_RGB(255, 255, 255)
    
    elif (0 < i <= 10):
        lcd.set_RGB(255, 0, 0)
        
    elif (10 < i <= 20):
        lcd.set_RGB(255, 127, 0)
        
    elif (20 < i <= 30):
        lcd.set_RGB(127, 127, 0)
        
    elif (30 < i <= 40):
        lcd.set_RGB(0, 255, 0)
        
    elif (40 < i <= 50):
        lcd.set_RGB(0, 255, 127)
        
    elif (50 < i <= 60):
        lcd.set_RGB(0, 127, 127)
        
    elif (60 < i <= 70):
        lcd.set_RGB(0, 127, 255)
        
    elif (70 < i <= 80):
        lcd.set_RGB(0, 0, 255)
        
    elif (80 < i <= 90):
        lcd.set_RGB(127, 0, 255)
    
    elif (90 < i <= 100):
        lcd.set_RGB(127, 0, 127)

    if (i >= 100):
        i = -20.0
   
    sleep_ms(100)
    
        
        






