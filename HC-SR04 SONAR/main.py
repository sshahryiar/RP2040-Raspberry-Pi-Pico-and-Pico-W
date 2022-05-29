from machine import Pin, Timer
from segment_display import seg_disp
from utime import sleep_ms, sleep_us, ticks_us
from SONAR import SONAR


seg = 0
value = 0


def timer_callback(t):
    global value, seg
    
    if(seg == 0):
        val = ((value % 10000) // 1000)
    elif(seg == 1):
        val = ((value % 1000) // 100)
    elif(seg == 2):
        val = ((value % 100) // 10)
    else:
        val = (value % 10)
    
    disp.send_data(val, seg, False)
    seg += 1
   
    if(seg > 3):
        seg = 0


tim = Timer(mode = Timer.PERIODIC, period = 1,  callback = timer_callback)
disp = seg_disp()
LED = Pin(25, Pin.OUT)
hcsr04 = SONAR(3, 2, 10, 38000, 5.8)


while(True):
    value = hcsr04.get_range()
    print(value)
    LED.toggle()
    sleep_ms(400)


