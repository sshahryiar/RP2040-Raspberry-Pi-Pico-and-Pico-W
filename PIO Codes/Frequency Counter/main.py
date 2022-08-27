from machine import Pin
from time import sleep_ms, ticks_us
from rp2 import asm_pio, StateMachine, PIO
from ST7789 import TFT114

t1 = 0
t2 = 0
t_diff = 0


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
    
    
sense_pin = Pin(0, Pin.IN)
tft = TFT114()
    
sm = StateMachine(0, IO_ops, in_base = sense_pin)
sm.irq(irq_0_handler)
sm.active(1)


def write_text(text, x, y, size, color):
        background = tft.pixel(x, y)
        info = []
        
        tft.text(text, x, y, color)
        for i in range(x, x + (8 * len(text))):
            for j in range(y, y + 8):
                px_color = tft.pixel(i, j)
                info.append((i, j, px_color)) if px_color == color else None
        
        tft.text(text, x, y, background)
       
        for px_info in info:
            tft.fill_rect(size*px_info[0] - (size-1)*x , size*px_info[1] - (size-1)*y, size, size, px_info[2]) 


while(True):
    period = t_diff
    tft.fill(tft.BLACK)
    write_text("RP2040 PICO PIO", 0, 6, 2, tft.WHITE)
    write_text("Frequency Meter", 0, 30, 2, tft.WHITE)
    
    if(period > 999):
        f = 1000000 / (period + 1)
        write_text("f/ Hz: " + str("%2.2f" %f), 2, 65, 2, tft.MAGENTA)
    else:
        f = 1000 / (period + 1)
        write_text("f/kHz: " + str("%2.2f" %f), 2, 65, 2, tft.MAGENTA)
    
    
    write_text("T/us : " + str("%4u" %period), 2, 105, 2, tft.CYAN)
    
    tft.show()

    sleep_ms(600)
    

