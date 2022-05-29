from micropython import const
from machine import UART
from utime import sleep_ms


ToF050_TX_data_packet_size = const(8)
ToF050_RX_data_packet_size = const(10)

ToF050_slave_default_ID = const(0x01)

#registers
ToF050_special_register = const(0x0001)
ToF050_slave_ID_register = const(0x0002)
ToF050_baud_rate_register = const(0x0003)
ToF050_range_precision_register = const(0x0004)
ToF050_output_control_register = const(0x0005)
ToF050_load_calibration_register = const(0x0006)
ToF050_offset_correction_register = const(0x0007)
ToF050_xtalk_correction_register = const(0x0008)
ToF050_i2c_enable_register = const(0x0009)
ToF050_measurement_register = const(0x0010)
ToF050_offset_calibration_register = const(0x0020)
ToF050_xtalk_calibration_register = const(0x0021)

#parameters
ToF050_restore_default = const(0xAA55)
ToF050_reboot = const(0x1000)
ToF050_comm_test = const(0x0000)

ToF050_baud_rate_115200 = const(0x0000)
ToF050_baud_rate_38400 = const(0x0001)
ToF050_baud_rate_9600 = const(0x0002)

ToF050_high_precision_20cm = const(0x0001)
ToF050_medium_precision_40cm = const(0x0002)
ToF050_low_precision_50cm = const(0x0003)

ToF050_do_not_load_calibration = const(0x0000)
ToF050_load_calibration = const(0x0001)

ToF050_i2c_not_prohibited = const(0x0000)
ToF050_i2c_prohibited = const(0x0001)

#other constant parameters
ToF050_default_max_distance = const(200)

MODBUS_read_holding_registers_function_code = const(0x03)
MODBUS_write_single_register_function_code = const(0x06)



class ToF050():
    def __init__(self, _uart):
        self.rx_data_frame = bytearray(ToF050_RX_data_packet_size)
        self.tx_data_frame = bytearray(ToF050_TX_data_packet_size)
        
        self.tof_slave_address = ToF050_slave_default_ID
        self.max_distance = ToF050_default_max_distance
        
        self.uart = _uart
        
        
    def generate_CRC16(self, value, length):
        n = 0
        s = 0
        crc_word = 0xFFFF
        
        for s in range (0x00, length):
            crc_word ^= value[s]
            
            for n in range (0x00, 0x08):
                if((crc_word & 0x0001) == 0):
                    crc_word >>= 1
                
                else:
                    crc_word >>= 1
                    crc_word ^= 0xA001
        
        return crc_word
    
    
    def check_crc(self, value, s, e):
        hb = value[e]
        lb = value[s]
        crc = hb
        crc <<= 8
        crc |= lb
        
        return crc
    
    
    def bytes_from_word(self, value):
        hb = 0x00
        lb = 0x00
        
        lb = (value & 0x00FF)
        hb = ((value & 0xFF00) >> 0x08)
        
        return hb, lb
        
    
    def MODBUS_TX(self, slave_ID, function_code, reg, value):
        crc = 0
        self.tx_data_frame[0x00] = slave_ID
        self.tx_data_frame[0x01] = function_code
        self.tx_data_frame[0x02], self.tx_data_frame[0x03] =  self.bytes_from_word(reg)
        self.tx_data_frame[0x04], self.tx_data_frame[0x05] = self.bytes_from_word(value)
        
        crc = self.generate_CRC16(self.tx_data_frame, 6)
        
        self.tx_data_frame[0x06] = (crc & 0x00FF)
        self.tx_data_frame[0x07] = ((crc & 0xFF00) >> 0x08)
        
        self.uart.write(self.tx_data_frame)
        sleep_ms(10)
        
    
    def MODBUS_RX(self, no_of_bytes_to_read):
        if(self.uart.any() > 0x00):
            self.rx_data_frame = self.uart.read()
            
            
    def get_range(self):
        crc_1 = 0x0000
        crc_2 = 0xFFFF
        range = -1        
        
        self.MODBUS_TX(self.tof_slave_address, MODBUS_read_holding_registers_function_code, ToF050_measurement_register, 0x0001)
        self.MODBUS_RX(0x07)
                
        if(self.rx_data_frame[0x00] == 0x01):
            if(self.rx_data_frame[0x01] == 0x03):
                if(self.rx_data_frame[0x02] == 0x02):
                    crc_1 = self.generate_CRC16(self.rx_data_frame, 5)
                    crc_2 = self.check_crc(self.rx_data_frame, 5, 6)
                    
                    if(crc_1 == crc_2):
                        range = self.rx_data_frame[3]
                        range <<= 0x08
                        range |= self.rx_data_frame[4]
                        
                    if(range > self.max_distance):
                        range = -1
                        
        return range
                        
        
