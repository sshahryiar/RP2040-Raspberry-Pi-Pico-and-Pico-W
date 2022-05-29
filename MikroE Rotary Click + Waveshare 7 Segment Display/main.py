from machine import Pin, Timer
from utime import sleep_ms
from encoder import encoder
from LED_circle import LED_circle
from segment_display import seg_disp


seg = 0
value = 0
invert = 0
counter = 1
past_value = 0
present_value = 0


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
led = LED_circle(21, 20, 7, 8)
enc = encoder(2, 3, 14, 0, 1000, 10)

led.send(0, 0)
sleep_ms(400)
led.send(0, 1)
sleep_ms(400)



while(True):
    if(enc.sw.value() == True):
        sleep_ms(40)
        if(enc.sw.value() == True):
            invert ^= 0x01    
    
    value = enc. decode()
    
    present_value = value
    
    if(present_value > past_value):
        counter += 1
    
    if(counter > 16):
        counter = 1
        
    if(present_value < past_value):
        counter -= 1
    
    if(counter < 1):
        counter = 16
        
    past_value = present_value
        
    led.send(counter, invert)
    print(value)    
    sleep_ms(100)





