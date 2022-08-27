from machine import Pin
from DHT import DHT2x
from ST7789 import TFT114
from utime import sleep_ms


LED = Pin(25, Pin.OUT)
dht = DHT2x(0)
tft = TFT114()



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
    LED.toggle()
    dht.get_reading()
    tft.fill(tft.BLACK)
    write_text("DHT11 PIO", 10, 4, 3, tft.CYAN)
    write_text(("RH/%: " + str("%2.1f" %dht.rh)), 0, 56, 3, tft.GREEN)
    write_text(("T/'C: " + str("%2.1f" %dht.t)), 0, 96, 3, tft.RED)
    tft.show()
    sleep_ms(400)
