from machine import Pin
from time import sleep_ms, ticks_us
from rp2 import asm_pio, StateMachine, PIO
from micropython import const


t1 = 0
t2 = 0
t_diff = 0


class TCS3200():
    
    @asm_pio()
    
    def IO_ops():
        irq(clear, 0)              # clear irq 0
        wait(1, pin, 0)            # wait for high logic on pin index 0, i.e sense pin
        irq(rel(0))                # raise IRQ 0
        wait(0, pin, 0)            # wait for logic low on pin index 0, i.e sense pin
        
        
    def irq_0_handler(sm):
        global t1, t2, t_diff
        t2 = ticks_us()
        t_diff = (t2 - t1)
        t1 = t2
    
    
    def __init__(self, _f_pin, _s0_pin, _s1_pin, _s2_pin, _s3_pin):
        self.LOW_POWER_MODE = const(0x00)
        self.F_2_PC_MODE = const(0x01)
        self.F_20_PC_MODE = const(0x02)
        self.F_100_PC_MODE = const(0x03)
        
        self.RED_FILTER = const(0x00)
        self.CLEAR_FILTER = const(0x01)
        self.BLUE_FILTER = const(0x02)
        self.GREEN_FILTER = const(0x03)
        
        
        self.f_pin = Pin(_f_pin, Pin.IN)
        self.s0_pin = Pin(_s0_pin, Pin.OUT)
        self.s1_pin = Pin(_s1_pin, Pin.OUT)
        self.s2_pin = Pin(_s2_pin, Pin.OUT)
        self.s3_pin = Pin(_s3_pin, Pin.OUT)
        
        self.sm = StateMachine(0,
                               TCS3200.IO_ops,
                               in_base = self.f_pin)
        
        self.sm.irq(TCS3200.irq_0_handler)
        
        
    def get_raw_reading(self, out_mode, filter_mode):
        global t_diff
        
        self.sm.active(0)
        
        if(out_mode == self.F_2_PC_MODE):
            self.s1_pin.off()
            self.s0_pin.on()
            
        elif(out_mode == self.F_20_PC_MODE):
            self.s1_pin.on()
            self.s0_pin.off()
        
        elif(out_mode == self.F_100_PC_MODE):
            self.s1_pin.on()
            self.s0_pin.on()
            
        else:
            self.s1_pin.off()
            self.s0_pin.off()
            
        if(filter_mode == self.CLEAR_FILTER):
            self.s3_pin.off()
            self.s2_pin.on()
            
        elif(filter_mode == self.BLUE_FILTER):
            self.s3_pin.on()
            self.s2_pin.off()
        
        elif(filter_mode == self.GREEN_FILTER):
            self.s3_pin.on()
            self.s2_pin.on()
            
        else:
            self.s3_pin.off()
            self.s2_pin.off()
            
        self.sm.active(1)    
        sleep_ms(100)
        
        period = t_diff + 1
        
        return period
    
    
    def get_color_reading(self):
        R = 0
        G = 0
        B = 0
        C = 0
        
        R = self.get_raw_reading(self.F_2_PC_MODE, self.RED_FILTER)
        G = self.get_raw_reading(self.F_2_PC_MODE, self.GREEN_FILTER)
        B = self.get_raw_reading(self.F_2_PC_MODE, self.BLUE_FILTER)
        C = self.get_raw_reading(self.F_2_PC_MODE, self.CLEAR_FILTER)
        
        return R, G, B, C
        
        
    def get_color_ratio(self):
        r = 0
        g = 0
        b = 0
        c = 0
        
        r, g, b, c = self.get_color_reading()
        
        r = int((c / r) * 100)
        g = int((c / g) * 100)
        b = int((c / b) * 100)
        
        c = (1000000 // c)
        
        return r, g, b, c      
