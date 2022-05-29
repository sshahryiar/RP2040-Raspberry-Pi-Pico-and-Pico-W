from machine import Pin, I2C
from I2C_LCD import TWI_LCD
import utime

lcd_port = I2C(1, scl=Pin(3), sda=Pin(2), freq=20_000)

print(lcd_port.scan())

i = -11.0

lcd = TWI_LCD(lcd_port, 0x27)

lcd.clr_home
lcd.goto_xy(1, 0)
lcd.put_str("RP2040 uPython")


while True:

    lcd.goto_xy(7, 1)
    lcd.put_str(str("%2.1f " % i))
    i += 0.1
    utime.sleep_ms(100)
    
    if(i >= 100):
        i = -11.0