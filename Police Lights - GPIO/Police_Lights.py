import machine
import utime

i = 0
state = 0

LED_RED = machine.Pin(4, machine.Pin.OUT)
LED_BLUE = machine.Pin(5, machine.Pin.OUT)

button = machine.Pin(2, machine.Pin.IN)


while True:
    if(button.value() == False):
        utime.sleep_ms(10)
        if(button.value() == False):
            LED_RED.value(False)
            LED_BLUE.value(False)
            state += 1

            
    if(state == 1):
        
        LED_RED.value(1)
        LED_BLUE.value(0)
        utime.sleep_ms(200)
        LED_RED.value(0)
        LED_BLUE.value(1)
        utime.sleep_ms(200)
    
    elif(state == 2):
        LED_RED.toggle()
        LED_BLUE.toggle()
        utime.sleep_ms(200)
        
    elif(state == 3):
        
        for i in range(0, 3, 1):
            LED_RED.value(1)
            LED_BLUE.value(0)
            utime.sleep_ms(40)
            LED_RED.value(0)
            utime.sleep_ms(40)
            
        for i in range(0, 3, 1):
            LED_RED.value(0)
            LED_BLUE.value(1)
            utime.sleep_ms(40)
            LED_BLUE.value(0)
            utime.sleep_ms(40)
            
            
    elif(state == 4):
        
         i = 6
         while(i > 0):
           LED_RED.on()
           LED_BLUE.on()
           utime.sleep_ms(60)
           LED_RED.off()
           LED_BLUE.off()
           utime.sleep_ms(60)
           i -= 1
           utime.sleep(0.25)
           
    else:
       LED_RED.value(0)
       LED_BLUE.value(0)
       utime.sleep_us(1000000)
       state = 0
    
