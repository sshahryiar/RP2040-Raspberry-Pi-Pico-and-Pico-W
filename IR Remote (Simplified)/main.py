from micropython import const
from machine import Pin
from utime import sleep_ms, sleep_us, ticks_diff, ticks_us, ticks_ms


pulse = const(1000)
sync_low = const(8000)
sync_high = const(16000)


ir_data = 0
temp = 0
first_edge = 0
second_edge = 0
capture_done = False


machine.freq(240000000)

IR_RX = Pin(14, Pin.IN)

LED1 = Pin(7, Pin.OUT)
LED2 = Pin(8, Pin.OUT)
LED3 = Pin(11, Pin.OUT)
LED4 = Pin(12, Pin.OUT)
LED_TGL = Pin(25, Pin.OUT)

LED1.value(False)
LED2.value(False)
LED3.value(False)
LED4.value(False)
LED_TGL.value(False)


while True:    

    if(IR_RX.value() == False):
        ir_data = 0
        temp = 0
        first_edge = 0
        second_edge = 0
        capture_done = False
        while(capture_done == False):
             
            print("IR Detected!")
            first_edge = ticks_us()
            
            i= 0
            while(IR_RX.value() == False):
                i += 1
                sleep_us(1)
                
                if(i > 2600):
                    break
                
            i = 0                
            while(IR_RX.value() == True):
                i += 1
                sleep_us(1)
                
                if(i > 2600):
                    break                
                
                
            second_edge = ticks_us()
            temp = ticks_diff(second_edge, first_edge)
            
            if(temp in range (sync_low, sync_high)):
                           
                 for s in range(0, 16):
                     LED_TGL.toggle()
                     ir_data <<= 1
                     first_edge = ticks_us()
                     while(IR_RX.value() == False):
                         continue
                        
                     while(IR_RX.value() == True):
                         continue
                     second_edge = ticks_us()
                     temp = ticks_diff(second_edge, first_edge)
                     
                     if(temp >= pulse):
                         ir_data |= 1                   
                    
                     print(str(s) + " " + str(temp))
                     
                 print("IR Data: " + str("%0x" % ir_data,))
                 
                 if((ir_data & 0x00FF) == 0x00EA):
                    LED1.toggle()
                 elif((ir_data & 0x00FF) == 0x00EE):
                    LED2.toggle()
                 elif((ir_data & 0x00FF) == 0x00E9):
                    LED3.toggle()
                 elif((ir_data & 0x00FF) == 0x00ED):
                    LED4.toggle()
                 elif((ir_data & 0x00FF) == 0x00E1):
                    LED1.value(False)
                    LED2.value(False)
                    LED3.value(False)
                    LED4.value(False)
                 
                 sleep_ms(100)
                 capture_done = True
                 
            else:
                print("Error!")
                capture_done = True                   

