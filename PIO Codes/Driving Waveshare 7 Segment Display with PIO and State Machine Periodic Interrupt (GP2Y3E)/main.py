from micropython import const
from machine import Pin, ADC
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


mosi_pin = const(11)
sck_pin = const(10)
rclk_pin = const(9)


seg = 0
value = 0


seg_code_list = [
    0x3F, # 0
    0x06, # 1
    0x5B, # 2
    0x4F, # 3
    0x66, # 4
    0x6D, # 5
    0x7D, # 6
    0x07, # 7
    0x7F, # 8
    0x6F, # 9
    0x77, # A
    0x7C, # b
    0x39, # C
    0x5E, # d
    0x79, # E
    0x71  # F
]

seg_pos_list = [
    0xFE, # 1st
    0xFD, # 2nd
    0xFB, # 3rd
    0xF7, # 4th  
]


@asm_pio(out_shiftdir = PIO.SHIFT_LEFT,
         autopull = True,
         pull_thresh = 16,
         out_init = PIO.OUT_LOW,
         sideset_init = (PIO.OUT_LOW, PIO.OUT_LOW))
    
def drive_display():
    
    wrap_target()
    set(x, 15)          .side(0b00)    # use x scratch register as a bit counter and clear RCLK and SCLK  
    label('loop')                      # data sending loop
    out(pins, 1)        .side(0b00)    # Toggle MOSI pin according to the bit value of MSB while holding SCLK and RCLK low
    jmp(x_dec, 'loop')  .side(0b10)    # Decrement x register value and set SCLK
    pull(ifempty)       .side(0b01)    # Pull data from TX_FIFO if empty and load new data to 74HC595s by setting RCLK high
    wrap()
    

sm1 = StateMachine(0, drive_display, freq = 1000000, out_base = Pin(mosi_pin), sideset_base = Pin(rclk_pin))
sm1.active(1)


def send_data(value, pos):
    temp = seg_pos_list[pos]
    temp <<= 8
    temp |= seg_code_list[value]
    
    sm1.put(temp << 16)


@asm_pio()

def periodic_irq():
    
    """
    Total Delay = (1 + (6 + 1) * (12 + 1 + 1) + 1) = 100 cycles
    Interrupt Frequency = 100000 / 100 = 1000 Hz
    
    """
    wrap_target()
    
    set(y, 6)            # Use y scratch register for loop count         
    
    label('loop')        # delay loop 
    nop() [12]           # 1 + 12 = 13 cycle delay
    jmp(y_dec, 'loop')   # decrement y scratch register and loopback
    
    irq(rel(0))          # if y scratch register is 0 then trigger interrupt
    wrap()


def periodic_irq_callback(sm):
    global seg
        
    point = False
    
    if(seg == 0):
        val = (value // 1000)
    elif(seg == 1):
        val = ((value % 1000) // 100)
        point = True
    elif(seg == 2):
        val = ((value % 100) // 10)
    else:
        val = (value % 10)
    
    send_data(val, seg)
    
    seg += 1
   
    if(seg > 3):
        seg = 0


sm2 = StateMachine(1, periodic_irq, freq = 100000)
sm2.irq(periodic_irq_callback)
sm2.active(1)


d_sensor = ADC(Pin(27))
state_pin = Pin(16, Pin.OUT)



while(True):
    d = 0
    avg = 0
    state_pin.on()
        
    for i in range (0, 8):
        avg += d_sensor.read_u16()
        sleep_ms(10)
        
    avg >>= 3
    
    state_pin.off()
    
    d = ((avg * 3300.0) / 65536.0)
    value = int(3140.25 - (d * 2.158))
    sleep_ms(400)

