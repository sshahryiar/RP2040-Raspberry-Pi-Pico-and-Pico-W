from micropython import const
from machine import Pin, SoftI2C
from utime import sleep_ms
from MAX44009 import MAX44009
from LCD import LCD


LCD_RS = const(22)
LCD_EN = const(10)
LCD_D4 = const(18)
LCD_D5 = const(11)
LCD_D6 = const(12)
LCD_D7 = const(28)


LED = Pin(25, Pin.OUT)
i2c = SoftI2C(scl=Pin(2), sda=Pin(3), freq=100000)
light = MAX44009(i2c)
lcd = LCD(LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7)


lcd.goto_xy(0, 0)
lcd.put_str("MAX44009  RP2040")
lcd.goto_xy(0, 1)
lcd.put_str("ALS/lux:")

while(True):
    lux = light.get_lux_value()
    lcd.goto_xy(9, 1)
    lcd.put_str(str("%5.1f " %lux))
    print(str("%5.1f" %lux))
    sleep_ms(400)