from machine import Pin
from rp2 import asm_pio, StateMachine, PIO
from utime import sleep_ms, sleep_us, ticks_us, ticks_diff


t1 = 0
t2 = 0
t_diff = 0


class SONAR():
    
    @asm_pio(sideset_init = PIO.OUT_LOW)
    def IO_ops():
        irq(clear, 0)              # clear irq 0
        irq(clear, 1)              # clear irq 1
        set(x, 9)                  # set x scratch register to count 10 (approximately 10 / 1000000 = 10us high time is needed for HC-SR04 to be triggred)
        nop() .side(1)             # wait one cycle and set the trigger pin high
        label("trigger")           # trigger delay start
        jmp(x_dec, "trigger")      # decement x scratch register value and loopback until x scratch register is zero
        nop() .side(0)             # wait one cycle and set the trigger pin low

        wait(1, pin, 0)            # wait for high logic on pin index 0, i.e echo pin
        irq(0)                     # set IRQ index 0 and wait for IRQ ack
        wait(0, pin, 0)            # wait for logic low on pin index 0, i.e echo pin
        irq(1)                     # set IRQ index 1 and wait for IRQ ack
        
        
    def irq_0_handler(sm):
        global t1, t2, t_diff
        t1 = 0
    
    
    def irq_1_handler(sm):
        global t1, t2, t_diff
        t2 = ticks_us()
        t_diff = ticks_diff(t2, t1)
        t1 = t2
        
        
    def get_reading_in_cm(self):
        global t_diff
        return (t_diff // 58)
    
    
    def get_reading_in_in(self):
        global t_diff
        return (t_diff // 148)
    
    
    def get_reading_us(self):
        global t_diff 
        return (t_diff)
    
        
    def __init__(self, _trigger_pin, _echo_pin, _sm = 0):
        self.sm = _sm
        
        self.ECHO_pin = Pin(_echo_pin, Pin.IN)
        self.TRIGGER_pin = Pin(_trigger_pin, Pin.OUT)
        
        self.sm = StateMachine(0, SONAR.IO_ops, in_base = self.ECHO_pin, sideset_base = self.TRIGGER_pin, freq = 1000000)

        self.sm.irq(SONAR.irq_0_handler)
        self.sm.irq(SONAR.irq_1_handler)

        self.sm.active(1)        
    

