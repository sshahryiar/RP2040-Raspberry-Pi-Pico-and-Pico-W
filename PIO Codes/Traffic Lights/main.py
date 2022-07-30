# LED blinking at approximately 16Hz


from machine import Pin
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


@asm_pio(set_init = (PIO.OUT_LOW, PIO.OUT_LOW, PIO.OUT_LOW))
def traffic_lights():
    label('loop')
    set(pins, 0b00001)
    
    set(x, 30)
    label("loop_R_1")
    set(y, 30)
    label("loop_R_2")
    nop() [31]
    jmp(y_dec, "loop_R_2")
    jmp(x_dec, "loop_R_1")
    
    
    set(pins, 0b00011)
    
    set(x, 20)
    label("loop_RY_1")
    set(y, 20)
    label("loop_RY_2")
    nop() [31]
    jmp(y_dec, "loop_RY_2")
    jmp(x_dec, "loop_RY_1")
    
    set(pins, 0b00100)
    
    set(x, 30)
    label("loop_G_1")
    set(y, 30)
    label("loop_G_2")
    nop() [31]
    jmp(y_dec, "loop_G_2")
    jmp(x_dec, "loop_G_1")
    
    
    set(pins, 0b00110)
    
    set(x, 20)
    label("loop_GY_1")
    set(y, 20)
    label("loop_GY_2")
    nop() [31]
    jmp(y_dec, "loop_GY_2")
    jmp(x_dec, "loop_GY_1")
    
    
    jmp('loop')
    

sm = StateMachine(0, traffic_lights, freq = 1920, set_base = Pin(2))

sm.active(1)
