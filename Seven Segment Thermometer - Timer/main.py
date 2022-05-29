from machine import Pin, Timer
from segment_display import seg_disp
from utime import sleep_ms


conversion_factor = 3.3 / 65535


seg = 0
value = 0


def timer_callback(t):
    global dat, seg
        
    point = False
    
    if(seg == 0):
        val = int(value / 100)
    elif(seg == 1):
        val = int((value % 100) / 10)
        point = True
    elif(seg == 2):
        val = int(value % 10)
    else:
        val = 12
    
    disp.send_data(val, seg, point)
    seg += 1
   
    if(seg > 3):
        seg = 0


tim = Timer(mode = Timer.PERIODIC, period = 1,  callback = timer_callback)
int_t_sensor = machine.ADC(4)
disp = seg_disp()


while(True):
    t_reading = int_t_sensor.read_u16() * conversion_factor 
    value = int((27 - (t_reading - 0.706) / 0.001721) * 10)
    sleep_ms(250)
