from machine import Pin, SPI, I2C
from SSD1306_I2C import OLED1306
from utime import sleep_ms, sleep_us
          
            
LED = Pin(26, Pin.OUT)
IR = Pin(18, Pin.IN, Pin.PULL_UP)


i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 100000)
oled = OLED1306(i2c)

oled.fill(oled.BLACK)
oled.show()


def poll_pulse(counts, pin_state):
    count = 0
    
    while(IR.value() == pin_state and count < counts):
        count += 1
        sleep_us(100)
        
    return count


while True:
    if(IR.value() == False):
        poll_pulse(120, False)
        poll_pulse(48, True)
        
       
        idx = 0
        cnt = 0
        data = [0, 0, 0, 0]    
       
        for i in range (0, 32):
            poll_pulse(9, False)
            pulse_len = poll_pulse(24, True)
            
            if(pulse_len > 5):
                data[idx] |= (1 << cnt)
               
            if(cnt == 7):
                cnt = 0
                idx += 1
            else:
                cnt += 1
               
            if(((data[0] + data[1]) == 0xFF) and ((data[2] + data[3]) == 0xFF)):
                LED.on()
                oled.fill(oled.BLACK)
                oled.text("IR Data:", 0, 10)
                oled.text(str("0x%02X" %data[0]), 0, 25)
                oled.text(str("%02X" %data[1]), 32, 25)
                oled.text(str("%02X" %data[2]), 48, 25)
                oled.text(str("%02X" %data[3]), 64, 25)
                oled.show()
                print("IR Data: 0x%02x" %data[0] + "%02x" %data[1] + "%02x" %data[2] + "%02x" %data[3])
                LED.off()

