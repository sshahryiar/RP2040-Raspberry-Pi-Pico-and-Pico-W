from machine import Pin, I2C
from utime import sleep_ms
from neopixel import NeoPixel
from HMC5883L import HMC5883L


pin = Pin(14, Pin.OUT) 
np = NeoPixel(pin, 24)

i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 100000)
compass = HMC5883L(i2c)


while(True):
    
    h = compass.get_heading()
    print(h)
    
    for i in range (0, 24):
        np[i] = (60, 0, 0)
    i = (h / 15)
    
    np[int(i)] = (0, 0 , 90)
    np.write()

    sleep_ms(400)