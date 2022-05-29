from micropython import const
from machine import Pin, PWM
from utime import sleep_ms, sleep_us


sleep_time = const(60)


D0 = Pin(1, Pin.OUT)
D1 = Pin(3, Pin.OUT)
D2 = Pin(5, Pin.OUT)
D3 = Pin(6, Pin.OUT)
D4 = Pin(7, Pin.OUT)
D5 = Pin(8, Pin.OUT)
D6 = Pin(9, Pin.OUT)
D7 = Pin(10, Pin.OUT)

pwm1 = PWM(Pin(0))
pwm1.freq(9000)

pwm2 = PWM(Pin(2))
pwm2.freq(9000)

pwm3 = PWM(Pin(4))
pwm3.freq(9000)


r_duty = [12043, 23676, 34503, 44155, 52302, 58668, 63036, 65256, 65254, 63028, 58656, 52286, 44135, 34481, 23652, 12017]
g_duty = [58668, 63036, 65256, 65254, 63028, 58656, 52286, 44135, 34481, 23652, 12017, 12043, 23676, 34503, 44155, 52302]
b_duty = [58656, 52286, 44135, 34481, 23652, 12017, 12043, 23676, 34503, 44155, 52302, 58668, 63036, 65256, 65254, 63028]


def level(value):
    if(value == 8):
        D0.low()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.high()
        D7.high()
    
    elif(value == 7):
        D0.high()
        D1.low()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.high()
        D7.high()
        
    elif(value == 6):
        D0.high()
        D1.high()
        D2.low()
        D3.high()
        D4.high()
        D5.high()
        D6.high()
        D7.high()
        
    elif(value == 5):
        D0.high()
        D1.high()
        D2.high()
        D3.low()
        D4.high()
        D5.high()
        D6.high()
        D7.high()
        
    elif(value == 4):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.low()
        D5.high()
        D6.high()
        D7.high()
        
    elif(value == 3):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.low()
        D6.high()
        D7.high()
        
    elif(value == 2):
        D0.high()
        D1.high()
        D2.high()
        D3.high()
        D4.high()
        D5.high()
        D6.low()
        D7.high()
        
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

        
while(True):
    for i in range(4, 9, 1):
        level(i)
        pwm1.duty_u16(r_duty[(i - 1)])
        pwm2.duty_u16(g_duty[(i - 1)])
        pwm3.duty_u16(b_duty[(i - 1)])
        sleep_ms(sleep_time)
        
    for i in range(8, 4, -1):
        level(i)
        pwm1.duty_u16(r_duty[(15 - i)])
        pwm2.duty_u16(g_duty[(15 - i)])
        pwm3.duty_u16(b_duty[(15 - i)])
        sleep_ms(sleep_time)
        
    for i in range(4, -1, -1):
        level(i)
        pwm1.duty_u16(r_duty[(15 - i)])
        pwm2.duty_u16(g_duty[(15 - i)])
        pwm3.duty_u16(b_duty[(15 - i)])
        sleep_ms(sleep_time)
        
    for i in range(1, 5, 1):
        level(i)
        pwm1.duty_u16(r_duty[(i - 1)])
        pwm2.duty_u16(g_duty[(i - 1)])
        pwm3.duty_u16(b_duty[(i - 1)])
        sleep_ms(sleep_time)
