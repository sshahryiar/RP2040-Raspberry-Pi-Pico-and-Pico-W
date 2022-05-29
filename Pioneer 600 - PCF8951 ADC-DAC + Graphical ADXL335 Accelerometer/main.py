from machine import Pin, I2C
from utime import sleep_ms
from PCF8591 import PCF8591
from SSD1306_I2C import OLED1306
import framebuf


LED = Pin(25, Pin.OUT)
i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 100000)
oled = OLED1306(i2c)
ad_da = PCF8591(i2c)


fb = framebuf.FrameBuffer(bytearray(
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'),
    36, 64, framebuf.MONO_VLSB)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def draw_background():
    oled.text("X", 2, 6, oled.WHITE)
    oled.text("Y", 2, 28, oled.WHITE)
    oled.text("Z", 2, 50, oled.WHITE)
    
    for i in range (0,  66, 22):
        oled.line(13, (10 + i), 91, (10 + i), oled.WHITE)
        oled.line(15, (1 + i), 15, (19 + i), oled.WHITE)
        oled.line(11, (2 + i), 13, (2 + i), oled.WHITE)
        oled.line(11, (18 + i), 13, (18 + i), oled.WHITE)
        oled.line(12, (1 + i), 12, (3 + i), oled.WHITE)
        


while True:
    oled.fill(oled.BLACK)
    draw_background()
    
    for i in range (16, 91):
        x_axis = ad_da.read(ad_da.AOut_disable | ad_da.Four_Channel_ADC | ad_da.Auto_Increment_Disable | ad_da.AIN0)
        y_axis = ad_da.read(ad_da.AOut_disable | ad_da.Four_Channel_ADC | ad_da.Auto_Increment_Disable | ad_da.AIN1)
        z_axis = ad_da.read(ad_da.AOut_disable | ad_da.Four_Channel_ADC | ad_da.Auto_Increment_Disable | ad_da.AIN2)
        
        x_plot = map_value(x_axis, 5, 220, 19, 1)
        y_plot = map_value(y_axis, 5, 220, 41, 23)
        z_plot = map_value(z_axis, 5, 220, 63, 45)
        
        oled.pixel(i, (x_plot), oled.WHITE)
        oled.pixel(i, (y_plot), oled.WHITE)
        oled.pixel(i, (z_plot), oled.WHITE)
        
        oled.blit(fb, 91, 0)
        
        oled.text(str("%3u" % x_axis), 100, 10, oled.WHITE)
        oled.text(str("%3u" % y_axis), 100, 30, oled.WHITE)
        oled.text(str("%3u" % z_axis), 100, 50, oled.WHITE)
        
        oled.show()
