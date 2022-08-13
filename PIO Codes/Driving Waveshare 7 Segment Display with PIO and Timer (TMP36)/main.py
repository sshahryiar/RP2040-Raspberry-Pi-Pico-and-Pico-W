from micropython import const
from machine import Pin, ADC, Timer
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


mosi_pin = const(11)
sck_pin = const(10)
rclk_pin = const(9)


conversion_factor = 3300 / 65535


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
    set(y, 15)          .side(0b00)  # use y scratch register as a bit counter and clear RCLK and SCLK  
    label('loop')                    # data sending loop
    out(pins, 1)        .side(0b00)  # Toggle MOSI pin according to the bit value of MSB while holding SCLK and RCLK low
    jmp(y_dec, 'loop')  .side(0b10)  # Decrement y register value and set SCLK
    pull(ifempty)       .side(0b01)  # Pull data from TX_FIFO if empty and load new data to 74HC595s by setting RCLK high
    wrap()
    

sm = StateMachine(0, drive_display, freq = 1000000, out_base = Pin(mosi_pin), sideset_base = Pin(rclk_pin))

sm.active(1)


def send_data(value, pos, dot):
    temp = seg_pos_list[pos]
    temp <<= 8
    temp |=  seg_code_list[value]
    
    if(dot == True):
        temp |= 0x80
    
    sm.put(temp << 16)
    

def timer_callback(t):
    global seg
        
    point = False
    
    if(seg == 0):
        val = int(value / 100)
    elif(seg == 1):
        val = int((value % 100) / 10)
        point = True
    elif(seg == 2):
        val = int(value % 10)
    else:
        val = 12
    
    send_data(val, seg, point)
    seg += 1
   
    if(seg > 3):
        seg = 0


tim = Timer(mode = Timer.PERIODIC, period = 1,  callback = timer_callback)
t_sensor = ADC(Pin(26))


while(True):
    avg = 0
    for i in range (0, 64):
        avg += t_sensor.read_u16()
        sleep_ms(4)
    avg >>= 6
    
    t_reading =  avg * conversion_factor
    value = (t_reading / 3)
    sleep_ms(250)

