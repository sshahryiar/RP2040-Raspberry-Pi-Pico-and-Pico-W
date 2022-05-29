from micropython import const
from machine import Pin, SoftSPI
from utime import sleep_ms
from TM1637 import TM1637
from MPL115A1 import MPL115A1

tm = TM1637(2, 3, 6)
spi = SoftSPI(baudrate=100000, polarity = 0, phase = 0, sck = Pin(12), mosi = Pin(11), miso=Pin(10))
baro = MPL115A1(spi, 8, 7)

while(True):
    P, T = baro.get_data()
    tm.put_str(0, str("%3u" %T))
    tm.put_str(3, " 'C")
    sleep_ms(1600)
    tm.put_str(0, str("%3u" %P))
    tm.put_str(3, "kPa")
    sleep_ms(1600)