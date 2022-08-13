from machine import Pin, ADC
from utime import sleep_ms
from rp2 import PIO, asm_pio, StateMachine


seg = 0
value = 0


seg_code_list = [
    0xC0, # 0
    0xF9, # 1
    0xA4, # 2
    0xB0, # 3
    0x99, # 4
    0x92, # 5
    0x82, # 6
    0xF8, # 7
    0x80, # 8
    0x90, # 9
    0x9C, # Degree Symbol 
]

seg_pos_list = [
    0x0E, # 1st
    0x0D, # 2nd
    0x0B, # 3rd
    0x07, # 4th  
]


@asm_pio(out_shiftdir = PIO.SHIFT_RIGHT,
         autopull = True,
         pull_thresh = 12,
         out_init = ((PIO.OUT_HIGH, ) * 12))
    
def drive_display():
    pull(ifempty)  # Pull data from TX_FIFO if empty
    out(pins, 12)
    

sm1 = StateMachine(0, drive_display, freq = 1000000, out_base = Pin(2))
sm1.active(1)


def send_data(value, pos):
    temp = seg_pos_list[pos]
    temp <<= 8
    temp |= seg_code_list[value]     
    sm1.put(temp)


@asm_pio()

def periodic_irq():
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
        val = (value // 100)
    elif(seg == 1):
        val = ((value % 100) // 10)
        point = True
    elif(seg == 2):
        val = (value % 10)
    else:
        val = 10
    
    send_data(val, seg)
    
    seg += 1
   
    if(seg > 3):
        seg = 0


sm2 = StateMachine(1, periodic_irq, freq = 100000)
sm2.irq(periodic_irq_callback)
sm2.active(1)

angle_sensor = ADC(Pin(28))


while(True):
    angle_sensor_value = 0 
    avg = 0
        
    for i in range (0, 16):
        avg += angle_sensor.read_u16()
        sleep_ms(10)
        
    avg >>= 4
    
    angle_sensor_value = ((avg * 360) / 65536)
    
    value = int(angle_sensor_value)
    sleep_ms(600)

