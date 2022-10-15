from machine import Pin, I2C
from utime import sleep_ms
from ST7789 import TFT2
from INA219 import INA219


key1 = Pin(15, Pin.IN, Pin.PULL_UP)
key2 = Pin(17, Pin.IN, Pin.PULL_UP)
LED = Pin(25, Pin.OUT)
i2c = I2C(1, scl = Pin(7), sda = Pin(6), freq = 100000)
ina = INA219(i2c, 0x43, 0.1, 2.95 , 4.2)
tft = TFT2()


state_1 = False
state_2 = False


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain_value(v, max_v, min_v):
    if(v >= max_v):
        v = max_v
    
    if(v <= min_v):
        v = min_v
        
    return v


def back_art(value):
    tft.fill(tft.BLACK)
    tft.text("Raspberry Pi PICO RP2040 UPS" , 40, 20, tft.WHITE)
    
    tft.fill_rect(20, 50, 30, 10, tft.WHITE)
    tft.rect(10, 60, 50, 170, tft.WHITE)
    tft.rect(12, 62, 46, 166, tft.WHITE)
    
    h1 = map_value(value, 0, 100, 225, 65)
    h2 = map_value(value, 0, 100, 0, 160)
    
    h1 = constrain_value(h1, 225, 65)
    h2 = constrain_value(h2, 160, 0)
    
    if(0 < value <= 30):
        colour = tft.RED
    elif(30 < value <= 60):
        colour = tft.YELLOW
    else:
        colour = tft.GREEN
        
    tft.fill_rect(15, h1, 40, h2, colour)
    
    
for i in range(0, 100, 5):
    back_art(i)
    tft.show()
    

for i in range(100, 0, -5):
    back_art(i)
    tft.show()


while (True):    
     
    if(key1.value() == False):
        LED.on()
        while(key1.value() == False):
            pass
        state_1 ^= 1
        LED.off()
        
    if(key2.value() == False):
        LED.on()
        while(key2.value() == False):
            pass
        state_2 ^= 1
        LED.off()
     
 
    bv = (ina.get_bus_voltage_in_mV() / 1000.0)        
    c = ina.get_battery_capacity()
    
    if(state_1):
        i = ina.get_current_mA()
    else:
        i = ina.get_current_from_shunt()
        
        
    if(state_2):
        p = ina.get_power()
    else:
        p = ina.calculate_power()
    
    back_art(c)
    
    tft.text("Battery Parameters" , 110, 55, tft.MAGENTA)
    tft.text(("Voltage : " + str("%1.3f" %bv) + " V"), 110, 80, tft.CYAN)
    tft.text(("Current : " + str("%4.1f" %i) + " mA"), 110, 110, tft.GREEN)
    tft.text(("Power   : " + str("%3.2f" %p) + " W"), 110, 140, tft.RED)
    tft.text(("Capacity: " + str("%3.1f" %c) + " %"), 110, 170, tft.YELLOW)
    
    tft.show()
    
    print("Voltage :  {:1.3f} V".format(bv))
    print("Current :  {:4.1f} mA".format(i))
    print("Power   :  {:3.2f} W".format(p))
    print("Capacity:  {:3.1f} %".format(c))
    print("\r\n")
    
    sleep_ms(100)
