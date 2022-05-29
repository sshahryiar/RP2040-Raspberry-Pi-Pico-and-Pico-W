from machine import Pin
from utime import sleep_us, ticks_us


class SONAR():
    def __init__(self, _trigger, _echo, _pulse_time, _timeout, _scaling_factor):
        self.timeout = _timeout
        self.pulse_time = _pulse_time
        self.scaling_factor = _scaling_factor
        self.echo = Pin(_echo, Pin.IN)
        self.trigger = Pin(_trigger, Pin.OUT)
        
        self.trigger.low()
        
        
    def trigger_sensor(self):
        self.trigger.high()
        sleep_us(self.pulse_time)
        self.trigger.low()
   
        
    def get_range(self):        
        self.trigger_sensor()
        
        cnt = 0
        while((cnt < self.timeout) and (self.echo.value() == False)):
            cnt += 1
            sleep_us(1)
        
        t1 = ticks_us()
        
        cnt = 0
        while((cnt < self.timeout) and (self.echo.value() == True)):
            cnt += 1
            sleep_us(1)
        
        t2 = ticks_us()
        
        d = (t2 - t1)
        if(d < 0):
            d  = 0
            
        d = int(d / self.scaling_factor)
        
        return d
        
