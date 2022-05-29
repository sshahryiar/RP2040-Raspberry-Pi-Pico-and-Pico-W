from machine import Pin


class encoder():
    
    def __init__(self, enc_A, enc_B, _sw, _min_cnt,  _max_cnt, _step_size):
        self.sw = Pin(_sw, Pin.IN)
        self.enc_a = Pin(enc_A, Pin.IN)
        self.enc_b = Pin(enc_B, Pin.IN)
        self.max_cnt = _max_cnt
        self.min_cnt = _min_cnt
        self.step_size = _step_size
        self.cnt = self.min_cnt
        
        
    def check_count(self):
        if self.enc_a.value():
            self.cnt += self.step_size
            
            if(self.cnt > self.max_cnt):
                self.cnt = self.min_cnt
                
        else:
            self.cnt -= self.step_size
            
            if(self.cnt < self.min_cnt):
                self.cnt = self.max_cnt
    
    
    def irq_handler_1(self, p):
        self.check_count()


    def irq_handler_2(self, p):
        self.check_count()
            
            
    def decode(self):
        if ((self.enc_a.value() == True) and (self.enc_b.value() == True)):
            self.enc_b.irq(self.irq_handler_1, Pin.IRQ_FALLING)
        
        if ((self.enc_a.value() == False) and (self.enc_b.value() == False)):
            self.enc_b.irq(self.irq_handler_2, Pin.IRQ_RISING)
            
        return self.cnt
                
