from machine import Pin, I2C
from I2C_LCD import TWI_LCD
from utime import sleep_ms, ticks_diff, ticks_us


lcd_port = I2C(1, scl=Pin(3), sda=Pin(2), freq=20_000)
lcd = TWI_LCD(lcd_port, 0x27)


f = 0
trap = True
t_diff = 0
first_edge = 0
second_edge = 0


interrupt_channel = Pin(15, Pin.IN)

def interrupt_handler(pin):
    global t_diff, trap, first_edge, second_edge
    
    interrupt_channel.irq(handler = None)
    
    if(trap == True):
        first_edge = ticks_us()
    else:
        second_edge = ticks_us()
        t_diff = ticks_diff(second_edge, first_edge)
        
    trap = not trap
    
    interrupt_channel.irq(handler = interrupt_handler)
    
interrupt_channel.irq(trigger = Pin.IRQ_FALLING, handler = interrupt_handler)


lcd.clr_home
lcd.goto_pos(0, 0)
lcd.put_str("Frequency/Hz:")


while True:    
    f = (500000 / (t_diff))
    print('F/Hz:' + str(f))
    lcd.goto_pos(0, 1)
    lcd.put_str(str("%4.2f            " % f))
    sleep_ms(100)

