from machine import Pin, I2C, SoftI2C
from SHTC3 import SHTC3
from SGP40 import SGP40
from SSD1306_mini import OLED96
from VOC_Algorithm import VOC_Algorithm
from utime import sleep_ms


sht_i2c = SoftI2C(scl = Pin(5, Pin.IN, Pin.PULL_UP), sda = Pin(4, Pin.IN, Pin.PULL_UP), freq = 400000)
oled_i2c = SoftI2C(scl = Pin(15, Pin.IN, Pin.PULL_UP), sda = Pin(14, Pin.IN, Pin.PULL_UP), freq = 400000)
sgp_i2c = SoftI2C(scl = Pin(17, Pin.IN, Pin.PULL_UP), sda = Pin(16, Pin.IN, Pin.PULL_UP), freq = 400000)


sht = SHTC3(sht_i2c)
oled = OLED96(oled_i2c)
sgp = SGP40(sgp_i2c)
voc = VOC_Algorithm()


while(True):    
    t, rh = sht.measure()
    raw_voc = sgp.raw_measurement(t, rh)
    voc.value = voc.VocAlgorithm_process(raw_voc)
    oled.fill(oled.BLACK)
    oled.text("Tmp/'C :" + str("%3.2f" %t), 1, 4, oled.WHITE)
    oled.text("R.H./% :" + str("%3.2f" %rh), 1, 14, oled.WHITE)
    oled.text("VoC/ppm:" + str("%3.2f" %voc.value), 1, 24, oled.WHITE)
    oled.show()
    sleep_ms(900)