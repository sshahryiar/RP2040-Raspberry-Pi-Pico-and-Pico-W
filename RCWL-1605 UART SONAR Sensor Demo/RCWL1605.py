from micropython import const
from machine import UART
from utime import sleep_ms


RCWL1605_measure_command = const(0xA0)
RCWL1605_device_info_command = const(0xF1)


class RCWL1605():
    def __init__ (self, _uart):
        self.tx_data_frame = bytearray(0x01)
        self.rx_data_frame = bytearray(0x1F)
        
        self.uart = _uart
        
        
    def get_distance(self):
        r = -1
        d = -1
        
        self.rx_data_frame[0x00] = 0x00
        self.rx_data_frame[0x01] = 0x00
        self.rx_data_frame[0x02] = 0x00
        
        self.tx_data_frame[0x00] = RCWL1605_measure_command
        self.uart.write(self.tx_data_frame)
        sleep_ms(10)
        
        if(self.uart.any() > 0x00):
            self.uart.readinto(self.rx_data_frame)
            r = ((self.rx_data_frame[0] << 0x10) + (self.rx_data_frame[1] << 0x08) + self.rx_data_frame[2])
            d = (r // 1000)
            
        return d
    
    
    def get_idevice_nfo(self):
        self.tx_data_frame[0x00] = RCWL1605_device_info_command
        self.uart.write(self.tx_data_frame)
        sleep_ms(10)
        
        if(uart.any() > 0x00):
            self.rx_data_frame = self.uart.read()
            
        return self.rx_data_frame
        