from machine import Pin, PWM, ADC
from utime import sleep_ms, sleep_us
import math


adc = ADC(Pin(26))

D0 = Pin(1, Pin.OUT)
D1 = Pin(3, Pin.OUT)
D2 = Pin(5, Pin.OUT)
D3 = Pin(6, Pin.OUT)
D4 = Pin(7, Pin.OUT)
D5 = Pin(8, Pin.OUT)
D6 = Pin(9, Pin.OUT)
D7 = Pin(10, Pin.OUT)

pwm1 = PWM(Pin(0))
pwm1.freq(6000)
pwm1.duty_u16(65536)

pwm2 = PWM(Pin(2))
pwm2.freq(6000)
pwm2.duty_u16(65536)

pwm3 = PWM(Pin(4))
pwm3.freq(6000)
pwm3.duty_u16(0)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min)/(x_max - x_min)) * (v - x_min)))


def level(value):
    if(value == 8):
        D0.low()
        D1.low()
        D2.low()
        D3.low()
        D4.low()
        D5.low()
        D6.low()
        D7.low()
    
    elif(value == 7):
        D0.high()
        D1.low()
        D2.low()
        D3.low()
        D4.low()
        D5.low()
        D6.low()
        D7.low()
        
    elif(value == 6):
        D0.high()
        D1.high()
        D2.low()
        D3.low()
        D4.low()
        D5.low()
        D6.low()
        D7.low()
        
    elif(value == 5):
        D0.high()
        D1.high()
        D2.high()
        D3.low()
        D4.low()
        D5.low()
        D6.low()
        D7.low()
        
    elif(value == 4):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.low()
        D5.low()
        D6.low()
        D7.low()
        
    elif(value == 3):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.low()
        D6.low()
        D7.low()
        
    elif(value == 2):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.low()
        D7.low()
        
    elif(value == 1):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.high()
        D7.low()
        
    else:
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.high()
        D7.high()
        
        
def ADC_rms():
    rms = 0
    tmp = 0
    sample = 0
    
    for i in range(0, 16):
        sample = adc.read_u16()
        tmp += (sample * sample)
        
    tmp >>= 4
    rms = math.sqrt(tmp)
    rms *= 0.000050354
    
    if(rms <= 0):
        rms = 0.000050354
        
    return rms


def get_dB():
    dB = ADC_rms()
    dB  = 94 + (20 * math.log10(dB / 3.16))
    return dB
        
        
while(True):
    db = get_dB()
    print(db)
    
    if((db >= 30) and (db <= 55)):
        pwm1.duty_u16(64000)
        pwm2.duty_u16(40)
        pwm3.duty_u16(64000)
       
    elif((db >55) and (db <= 75)):
        pwm1.duty_u16(64000)
        pwm2.duty_u16(40)
        pwm3.duty_u16(64000)
        
    else:
        pwm1.duty_u16(40)
        pwm2.duty_u16(64000)
        pwm3.duty_u16(64000)
        
    i = map_value(db, 40, 90, 1, 8)
    level(i)
    sleep_ms(40)
  


