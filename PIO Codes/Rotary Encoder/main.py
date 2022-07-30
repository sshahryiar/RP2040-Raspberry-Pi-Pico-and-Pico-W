from machine import Pin
from SH1107 import OLED_13
from utime import sleep_ms
from rp2 import asm_pio, StateMachine, PIO


count = 0
direction = 0


@asm_pio(set_init = (PIO.IN_HIGH, PIO.IN_HIGH))
def rotary_encoder():
    irq(clear, 0)    # clear IRQ 0
    wrap_target()
    wait(0, pin, 1)  # wait input_pins(1) goes LOW
    in_(pins, 2)     # read input_pins into ISR
    push(block)      # push ISR to RX FIFO
    irq(0)           # raise IRQ 0
    wait(1, pin, 1)  # wait input_pins(1) goes HIGH
    wrap()
    

def irq_callback(sm):
    global count, direction
    
    if (sm.irq().flags() > 0):
        
        direction = sm.get()
        
        LED.toggle()
        
        if(direction == 0): 
            count += 1
        else: 
            count -= 1


LED = Pin(25, Pin.OUT)

oled = OLED_13()

sm = StateMachine(0, rotary_encoder, in_base = Pin(18), freq = 25000)
sm.irq(irq_callback)
sm.active(1) 


while(True):
    oled.fill(oled.BLACK)
    
    oled.text("Count:", 6, 10, oled.WHITE)
    oled.text("Direction:", 6, 25, oled.WHITE)
    
    if(count > 9999):
        count = 0
    elif(count < 0):
        count = 9999
    
    oled.text(str("% 4u" % count), 45, 10, oled.WHITE)
    
    if(direction == 0):
        oled.text("UP", 86, 25, oled.WHITE)
    else:
        oled.text("DOWN", 86, 25, oled.WHITE)
    
    oled.show()
    sleep_ms(100)

    

