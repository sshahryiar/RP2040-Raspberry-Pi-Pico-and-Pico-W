from micropython import const
from machine import UART, Pin
from utime import sleep_ms


HMC1022_I2C_Address = const(0xE0) 
                                                                          
HMC1022_Get_Angular_Measurement = const(0x31)
HMC1022_Start_Calibration = const(0xC0)  
HMC1022_End_Calibration = const(0xC1)                      
HMC1022_Set_Magnetic_Declination_High_Byte = const(0x03)   
HMC1022_Set_Magnetic_Declination_Low_Byte = const(0x04)
                
HMC1022_max_no_of_bytes_to_send = const(0x04)
HMC1022_max_no_of_bytes_to_read = const(0x08)


class HMC1022():
    def __init__(self, _uart, _pin):
        self.tx_data = bytearray(HMC1022_max_no_of_bytes_to_send)
        self.rx_data = bytearray(HMC1022_max_no_of_bytes_to_read)
        self.calibration_LED = Pin(_pin, Pin.OUT)
        self.uart = _uart
        
    
    def get_heading(self):
        i = 0x00
        h = -1
        CRC = 0x00
        temp = bytearray(HMC1022_max_no_of_bytes_to_read)
        
        self.tx_data[0x00] = HMC1022_Get_Angular_Measurement
        self.tx_data[0x01] = 0x00
        self.tx_data[0x02] = 0x00
        self.tx_data[0x03] = 0x00
        
        self.uart.write(self.tx_data)
        
        if(self.uart.any() > 0x00):
            self.rx_data = self.uart.read(HMC1022_max_no_of_bytes_to_read)
        
        if(self.rx_data[0x00] == 0x0D):
            if(self.rx_data[0x01] == 0x0A):
                if(self.rx_data[0x05] == 0x2E):
                    for i in range (0x00, 0x07):
                        CRC += self.rx_data[i]
                    
                    if((CRC & 0xFF) == self.rx_data[0x07]):
                        for i in range (0x02, 0x07):
                            temp[i] = (self.rx_data[i] - 0x30)
                            
                        h = (float(temp[0x02]) * 100.0)
                        h += (float(temp[0x03]) * 10.0)
                        h += (float(temp[0x04]) * 1.0)
                        h += (float(temp[0x06]) * 0.1)
                    
                    else:
                        h = -1
                    
        return h
    
    
    def calibrate(self):
        i = 0
        self.tx_data[0x00] = HMC1022_Start_Calibration
        self.tx_data[0x01] = 0x00
        self.tx_data[0x02] = 0x00
        self.tx_data[0x03] = 0x00
        
        self.uart.write(self.tx_data)
        
        for i in range (0, 60):
            self.calibration_LED.on()
            sleep_ms(100)
            self.calibration_LED.off()
            sleep_ms(990)
        
        for i in range (0, 60):
            self.calibration_LED.on()
            sleep_ms(400)
            self.calibration_LED.off()
            sleep_ms(600)
            
        self.tx_data[0x00] = HMC1022_End_Calibration
        self.uart.write(self.tx_data)
        
        
    def factory_reset(self):
        self.tx_data[0x00] = 0xA0
        self.tx_data[0x01] = 0xAA
        self.tx_data[0x02] = 0xA5
        self.tx_data[0x03] = 0xC5
        
        self.uart.write(self.tx_data)
        
        
    def set_I2C_address(self, new_I2C_address):
        self.tx_data[0x00] = 0xA0
        self.tx_data[0x01] = 0xAA
        self.tx_data[0x02] = 0xA5
        self.tx_data[0x03] = new_I2C_address
        
        self.uart.write(self.tx_data)
        
        
    def set_declination_angle(self, angle):
        hb = 0x00
        lb = 0x00
        
        lb = (angle & 0x00FF) 
                             
        hb = (angle & 0xFF00)
        hb >>= 0x08
        
        self.tx_data[0x00] = HMC1022_Set_Magnetic_Declination_High_Byte
        self.tx_data[0x01] = hb
        self.tx_data[0x02] = HMC1022_Set_Magnetic_Declination_Low_Byte
        self.tx_data[0x03] = lb
        
        self.uart.write(self.tx_data)
        
            

