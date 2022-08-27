from micropython import const
from machine import Pin
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


DHT11_sensor = const(0)
DHT2x_sensor = const(1)


class DHT():

    @asm_pio(set_init = PIO.OUT_HIGH,
             in_shiftdir = PIO.SHIFT_LEFT,
             push_thresh = 8,
             autopush = True)

    def io_ops():
        set(pindirs, 1)                # Set the sensor pin as an output
        set(pins, 0)                   # Set the pin low
        set(x, 20)                     # Create a delay of approximately 10000 cycles or 10000 / 500000 = 20ms 
        label('loop1')                 # while holding the pin low
        set(y, 20)
        label('loop2')
        nop() [22]
        jmp(y_dec, 'loop2')
        jmp(x_dec, 'loop1')
        
        set(pindirs, 0)
        wait(1, pin, 0) 
        wait(0, pin, 0) 
        wait(1, pin, 0) 

        set(x, 4)
        label('bytes')
        set(y, 7)
        label('bits')
        wait(0, pin, 0) 
        wait(1, pin, 0) [24]
        in_(pins, 1)
        jmp(y_dec, 'bits')
        jmp(x_dec, 'bytes')
        


    def __init__(self, _pin, _sensor, _sm = 0):
        self.pin = Pin(_pin, Pin.IN, Pin.PULL_UP)
        self.rh = 0
        self.t = 0
        self.checksum = 0
        self.sensor = _sensor
        self.sm = StateMachine(_sm, DHT.io_ops,
                               freq = 500000,
                               in_base = self.pin,
                               set_base = self.pin)
    	self.sm.active(1)
    	
   
    def get_reading(self):
        data = []
        
        self.sm.restart()

        for i in range(0, 5):
            data.append(self.sm.get())

        self.checksum = ((data[0] + data[1] + data[2] + data[3]) & 0xFF)

        if(data[4] == self.checksum):
            if(self.sensor == DHT2x_sensor):
                sign = 0
                
                if(data[2] & 0x80):
                    sign = -1
                    
                else:
                    sign = 1
                
                self.rh = (((data[0] << 8) + data[1]) / 10)
                self.t = (((((data[2] & 0x7F) << 8) + data[3]) * sign) / 10)
                
            else:
                self.rh = (data[0] + (data[1] / 100))
                self.t = (data[2] + (data[3] / 100))
        
       


class DHT11(DHT):
    def __init__(self, pin, sm = 0):
        super().__init__(pin, DHT11_sensor, sm)


class DHT2x(DHT):
    def __init__(self, pin, sm = 0):
        super().__init__(pin, DHT2x_sensor, sm)




