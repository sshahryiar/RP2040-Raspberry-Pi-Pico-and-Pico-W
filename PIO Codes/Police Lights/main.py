from machine import Pin
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


@asm_pio(set_init = PIO.OUT_LOW, sideset_init = PIO.OUT_HIGH)
def police_lights():
    wrap_target()
    
    set(pins, 0) .side(1)

    set(x, 29)
    label("delay_1")
    nop() [6]
    jmp(x_dec, "delay_1")
    
    set(pins, 1) .side(0)
    
    set(y, 29)
    label("delay_2")
    nop() [6]
    jmp(y_dec, "delay_2")
    
    wrap()
    

sm = StateMachine(0, police_lights, freq = 2000, set_base = Pin(2), sideset_base = Pin(3))

sm.active(1)