from micropython import const
from machine import Pin
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


DHT11_sensor = const(0)
DHT2x_sensor = const(1)


class DHT():

    @asm_pio(set_init = PIO.OUT_HIGH,
             in_shiftdir = PIO.SHIFT_LEFT,
             autopush = True)

    def io_ops():
        set(pindirs, 1)                # Set the sensor pin as an output
        set(pins, 1)                   # Set the pin high
        nop() [2]                      # Wait a bit
        set(pins, 0)                   # Set the pin low
        set(x, 20)                     # Create a delay of approximately 12000 cycles or 12000 / 500000 = 24ms 
        label('loop1')                 # while holding the pin low
        set(y, 20)
        label('loop2')
        nop() [26]
        jmp(y_dec, 'loop2')
        jmp(x_dec, 'loop1')

        set(pindirs, 0)                # Set sensor pin as an input
        wait(1, pin, 0)                # Wait for a high level response from the sensor
        wait(0, pin, 0)                # Wait for a low level response from the sensor
        wait(1, pin, 0)                # Wait for a high level response from the sensor
        wait(0, pin, 0)                # Wait for a low level response from the sensor

        set(x, 4)                      # Start recording 5 bytes of sensor data output
        label('bytes')
        set(y, 7)                      # Each byte contains 8 bits
        label('bits')
        wait(1, pin, 0)     [25]       # Wait for a high level response from the sensor and the wait for 25 / 500000 = 50us
        in_(pins, 1)                   # After 50us if the sensor is sending high out put then fill ISR with 1 or else fill with 0 and shift by 1 bit 
        wait(0, pin, 0)                # Wait for a low level response from the sensor       
        jmp(y_dec, 'bits')
        jmp(x_dec, 'bytes')
        
        push(block)                    # Finally push data out of RX_FIFO


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
        self.sm.restart()
        value = self.sm.get()
        CRC = (self.sm.get() & 0xFF)
        
        byte_1 = ((value >> 24) & 0xFF)
        byte_2 = ((value >> 16) & 0xFF)
        byte_3 = ((value >> 8) & 0xFF)
        byte_4 = (value & 0xFF)

        self.checksum = (byte_1 + byte_2 + byte_3 + byte_4)

        if(self.checksum == CRC):
            sleep_ms(800)
            if(self.sensor == DHT2x_sensor):
                sign = 0
                
                if(byte_3 & 0x80):
                    sign = -1
                    
                else:
                    sign = 1
                
                self.rh = (((byte_1 << 8) + byte_2) / 10)
                self.t = (((((byte_3 & 0x7F) << 8) + byte_4) * sign) / 10)
                
            else:
                self.rh = (byte_1 + (byte_2 / 100))
                self.t = (byte_3 + (byte_4 / 100))
        
       


class DHT11(DHT):
    def __init__(self, pin, sm = 0):
        super().__init__(pin, DHT11_sensor, sm)


class DHT2x(DHT):
    def __init__(self, pin, sm = 0):
        super().__init__(pin, DHT2x_sensor, sm)



