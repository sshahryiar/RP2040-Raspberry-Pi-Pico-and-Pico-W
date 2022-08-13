from micropython import const
from machine import Pin, ADC
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine
import dht


DAT_pin = const(16)
CLK_pin = const(17)


seg = 0
value_1 = 1234
value_2 = 5678


seg_code_list = [
    0x03,  # 0
    0x9F,  # 1
    0x25,  # 2
    0x0D,  # 3
    0x99,  # 4
    0x49,  # 5
    0x41,  # 6
    0x1F,  # 7
    0x01,  # 8
    0x09,  # 9  
]

seg_pos_list = [
    #Segment locations from top to bottom
    0x80, 
    0x40,
    0x20,
    0x10,
    0x08,
    0x04,
    0x02,
    0x01,
]


@asm_pio(out_shiftdir = PIO.SHIFT_RIGHT,
         autopull = True,
         pull_thresh = 16,
         out_init = PIO.OUT_LOW,
         sideset_init = PIO.OUT_HIGH)
    
def drive_display():
    
    wrap_target()
    set(y, 15)                    # use y scratch register as a bit counter
    label('loop')                 # data sending loop
    out(pins, 1)                  # Toggle the state of DAT pin according to the bit value of LSB
    nop()               .side(1)  # Wait a bit and set CLK pin high
    jmp(y_dec, 'loop')  .side(0)  # Decrement y register value and set CLK pin low
    pull(ifempty)                 # Pull data from TX_FIFO if empty and load new data to 74HC164 ICs
    wrap()
    

sm1 = StateMachine(0, drive_display, freq = 10000000, out_base = Pin(DAT_pin), sideset_base = Pin(CLK_pin))
sm1.active(1)


def send_data(value, pos, point):
    temp = seg_pos_list[pos]
    temp <<= 8
    temp |= seg_code_list[value]
    
    if(point == True):
        temp &= 0xFFFE
        
    sm1.put(temp)


@asm_pio()

def periodic_irq():
    
    """
    Total Delay = (1 + (6 + 1) * (12 + 1 + 1) + 1) = 100 cycles
    Interrupt Frequency = 100000 / 100 = 1000 Hz
    
    """
    wrap_target()
    
    set(x, 6)            # Use x scratch register for loop count         
    
    label('loop')        # delay loop 
    nop() [12]           # 1 + 12 = 13 cycle delay
    jmp(x_dec, 'loop')   # decrement x scratch register and loopback
    
    irq(rel(0))          # if x scratch register is 0 then trigger interrupt
    wrap()


def periodic_irq_callback(sm):
    global seg
        
    point = False
    
    if(seg == 0):
        send_data((value_1 // 1000), 0, False)
    elif(seg == 1):
        send_data(((value_1 % 1000) // 100), 1, True)
    elif(seg == 2):
        send_data(((value_1 % 100) // 10), 2, False)
    elif(seg == 3):
        send_data((value_1 % 10), 3, False)
    elif(seg == 4):
        send_data((value_2 // 1000), 4, False)
    elif(seg == 5):
        send_data(((value_2 % 1000) // 100), 5, True)
    elif(seg == 6):
        send_data(((value_2 % 100) // 10), 6, False)
    else:
        send_data((value_2 % 10), 7, False)

    seg += 1
   
    if(seg > 7):
        seg = 0


sm2 = StateMachine(1, periodic_irq, freq = 100000)
sm2.irq(periodic_irq_callback)
sm2.active(1)


DHT = dht.DHT11(Pin(0, Pin.IN))


while(True):
    DHT.measure()
    t = DHT.temperature()
    rh = DHT.humidity()
    
    value_1 = int(t * 100)
    value_2 = int(rh * 100)
    
    sleep_ms(400)


