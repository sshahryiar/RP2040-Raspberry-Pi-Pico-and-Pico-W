from micropython import const
from machine import Pin, ADC, SoftSPI
from utime import sleep_ms
from MAX72xx import MAX72xx


adc0 = ADC(Pin(26))
adc1 = ADC(Pin(27))

spi = SoftSPI(baudrate=100000, polarity = 0, phase = 0, sck = Pin(10), mosi = Pin(12), miso = Pin(25))
dis = MAX72xx(spi, 11)


def map_value_float(v, x_min, x_max, y_min, y_max):
    return (y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain_value(v, max_v, min_v):
    if(v >= max_v):
        v = max_v
    
    if(v <= min_v):
        v = min_v
        
    return v
    

def display_data(pos, value):
    dis.write((pos + 2), (value // 100))
    dis.write((pos + 1), (((value // 10) % 10) | 0x80))
    dis.write(pos, (value % 10))
    
    
def adc0_avg():
    avg = 0
    for i in range (0, 64):
        avg += adc0.read_u16()
        
    return (avg >> 6)


def adc1_avg():
    avg = 0
    for i in range (0, 64):
        avg += adc1.read_u16()
        
    return (avg >> 6)


while(True):
    T0 = adc0_avg()
    T0 = map_value_float(T0, 0, 65535, 0, 320)
    T0 = constrain_value(T0,  99.9, 0)
    display_data(6, int(T0 * 10))
    print("LM35 T0: " + str("%2.1f" %T0))
    
    T1 = adc1_avg()
    T1 = map_value_float(T1, 0, 65535, 0, 320)
    T1 = constrain_value(T1, 99.9, 0)
    display_data(1, int(T1 * 10))        
    print("LM35 T1: " + str("%2.1f" %T1))
    
    print("\r\n")
    sleep_ms(400)