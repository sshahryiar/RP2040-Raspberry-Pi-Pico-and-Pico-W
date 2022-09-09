from machine import Pin
from utime import sleep_ms
from neopixel import NeoPixel
from ST7789 import TFT208
from XPT2046 import touch


cal = 0
x_cal_min = 511
x_cal_max = 4095
y_cal_min = 4095
y_cal_max = 511
R_value = 0
G_value = 0
B_value = 0
R_slider = 40
G_slider = 40
B_slider = 40


tft = TFT208()
xpt = touch()
pin = Pin(0, Pin.OUT) 
RGB_LED = NeoPixel(pin, 1)



tft.fill(tft.BLACK)
tft.text("TFT Touch Calibration Point 1", 40, 100, tft.WHITE)
tft.rect(1, 1, 4, 4, tft.WHITE)
tft.show()
cal = 10
while(cal > 0):
    x_cal_1, y_cal_1 =  xpt.read_coordinates()
    cal -= 1
    sleep_ms(400)

print("x_1: " + str(x_cal_1) + "    y_1: " + str(y_cal_1))
tft.text(("X: " + str(x_cal_1) + " Y: " + str(y_cal_1)), 100, 140, tft.WHITE)
tft.show()
sleep_ms(1200)

tft.fill(tft.BLACK)
tft.text("TFT Touch Calibration Point 2", 40, 100, tft.WHITE)
tft.rect(316, 236, 4, 4, tft.WHITE)
tft.show()

cal = 10

while(cal > 0):
    x_cal_2, y_cal_2 =  xpt.read_coordinates()
    cal -= 1
    sleep_ms(400)
    
print("x_2: " + str(x_cal_2) + "    y_2: " + str(y_cal_2))
tft.text(("X: " + str(x_cal_2) + " Y: " + str(y_cal_2)), 100, 140, tft.WHITE)
tft.show()
sleep_ms(1200)


tft.fill(tft.BLACK)
tft.text("TFT Touch Calibration Point 3", 40, 100, tft.WHITE)
tft.rect(1, 236, 4, 4, tft.WHITE)
tft.show()

cal = 10

while(cal > 0):
    x_cal_3, y_cal_3 =  xpt.read_coordinates()
    cal -= 1
    sleep_ms(400)
    
print("x_3: " + str(x_cal_3) + "    y_3: " + str(y_cal_3))
tft.text(("X: " + str(x_cal_3) + " Y: " + str(y_cal_3)), 100, 140, tft.WHITE)
tft.show()
sleep_ms(1200)


tft.fill(tft.BLACK)
tft.text("TFT Touch Calibration Point 4", 40, 100, tft.WHITE)
tft.rect(316, 1, 4, 4, tft.WHITE)
tft.show()

cal = 10

while(cal > 0):
    x_cal_4, y_cal_4 =  xpt.read_coordinates()
    cal -= 1
    sleep_ms(400)
    
print("x_4: " + str(x_cal_4) + "    y_4: " + str(y_cal_4))
tft.text(("X: " + str(x_cal_4) + " Y: " + str(y_cal_4)), 100, 140, tft.WHITE)
tft.show()
sleep_ms(1200)

x_cal_min = ((x_cal_1 + x_cal_3) // 2)
x_cal_max = ((x_cal_2 + x_cal_4) // 2)

y_cal_min = ((y_cal_1 + y_cal_4) // 2)
y_cal_max = ((y_cal_2 + y_cal_3) // 2)

xpt.calibration(x_cal_min, y_cal_min, x_cal_max, y_cal_max)


while(True):
    tft.fill(tft.BLACK)
    
    tft.text("XPT2046 - RP2040 RGB Colour Generator", 10, 6, tft.WHITE)
    
    tft.fill_rect(42, 60, 100, 10, tft.WHITE)
    tft.fill_rect(42, 130, 100, 10, tft.WHITE)
    tft.fill_rect(42, 200, 100, 10, tft.WHITE)
    
    x_axis, y_axis = xpt.get_xy()
    
    if(40 <= y_axis <= 70):
        if(40 <= x_axis <= 140):
            R_slider = x_axis            
            R_value = xpt.map_value(R_slider, 40, 140, 0, 255)
            
    if(130 <= y_axis <= 150):
        if(40 <= x_axis <= 140):
            G_slider = x_axis
            G_value = xpt.map_value(G_slider, 40, 140, 0, 255)
            
    if(200 <= y_axis <= 240):
        if(40 <= x_axis <= 140):
            B_slider = x_axis
            B_value = xpt.map_value(B_slider, 40, 140, 0, 255)
            
    tft.fill_rect(R_slider, 55, 4, 20, tft.RED)
    tft.fill_rect(G_slider, 125, 4, 20, tft.GREEN)
    tft.fill_rect(B_slider, 195, 4, 20, tft.BLUE)
    
    tft.text("R", 20, 60, tft.RED)
    tft.text("G", 20, 130, tft.GREEN)
    tft.text("B", 20, 200, tft.BLUE)
    
    tft.text(str("%3u" %R_value), 160, 60, tft.RED)
    tft.text(str("%3u" %G_value), 160, 130, tft.GREEN)
    tft.text(str("%3u" %B_value), 160, 200, tft.BLUE)
    
    tft.fill_rect(240, 100, 60, 60, tft.colour_generator(R_value, G_value, B_value))
    
    tft.text(("0x" + str("%04X" %tft.colour_generator(R_value, G_value, B_value))), 245, 180, tft.WHITE)

    tft.show()
    
    RGB_LED[0] = (R_value, G_value, B_value)
    RGB_LED.write()

