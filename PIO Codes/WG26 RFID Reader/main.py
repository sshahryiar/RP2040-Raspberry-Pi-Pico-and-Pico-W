from machine import Pin
from SH1107 import OLED_13
from utime import sleep_ms
from rp2 import asm_pio, StateMachine, PIO


count = 0
raw_card_data = 0


@asm_pio()
def D0_out():
    irq(clear, 0)
    wrap_target()
    wait(0, pin, 0)  # wait for logic 0 on pin index 0
    irq(block, 0)    # set IRQ index 0 and wait for IRQ ack
    wait(1, pin, 0)  # wait for logic 1 on pin index 0
    wrap()


@asm_pio()
def D1_out():
    irq(clear, 1)
    wait(0, pin, 0)  # wait for logic 0 on pin index 0
    wrap_target()
    wait(1, pin, 0)  # wait for logic 1 on pin index 0
    irq(block, 1)    # set IRQ index 1 and wait for IRQ ack
    wait(0, pin, 0)  # wait for logic 0 on pin index 0
    wrap()
    

def irq_0_handler(sm):
    global raw_card_data, count
    
    raw_card_data <<= 1
    count += 1
    
    
def irq_1_handler(sm):
    global raw_card_data, count
    
    raw_card_data <<= 1
    count += 1
    raw_card_data |= 1


LED = Pin(25, Pin.OUT)
D0_pin = Pin(16, Pin.IN, Pin.PULL_UP)
D1_pin = Pin(17, Pin.IN, Pin.PULL_UP)


oled = OLED_13()

oled.fill(oled.BLACK)
oled.show()

sm0 = StateMachine(0, D0_out, in_base = D0_pin, freq = 45000)
sm1 = StateMachine(1, D1_out, in_base = D1_pin, freq = 45000)

sm0.irq(irq_0_handler)
sm1.irq(irq_1_handler)

sm0.active(1) # run SM0
sm1.active(1) # run SM1


while(True):
        
    if(count >= 25):
        sm0.active(0) 
        sm1.active(0)
        oled.fill(oled.BLACK)    
        oled.text("Facility Code :", 1, 10, oled.WHITE)
        oled.text("ID Card Number:", 1, 40, oled.WHITE)
        card_number = (raw_card_data & 0xFFFF)
        facility_code = (0xFF & (raw_card_data >> 0x10))
        oled.text(str("%u" % facility_code), 1, 20, oled.WHITE)
        oled.text(str("%u" % card_number), 1, 50, oled.WHITE)
        oled.show()
        sleep_ms(100)
        raw_card_data = 0
        count = 0
        sm0.active(1) 
        sm1.active(1)