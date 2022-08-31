from micropython import const
from machine import UART
from utime import sleep_ms


GY68x_TX_data_packet_size = const(4)
GY68x_RX_data_packet_size = const(20)

GY68x_RX_buffer_size = const(40)

GY68x_data_request_cmd = const(0x55)


GY68x_data_output_cmd = const(0x56)

GY68x_data_output_auto = const(0x02)
GY68x_data_output_manual = const(0x01)


GY68x_baud_rate_cmd = const(0x58)

GY68x_9600_baud = const(0x02)
GY68x_115200_baud = const(0x01)


GY68x_save_restore_setup_cmd = const(0x5A)

GY68x_save_setup = const(0x01)
GY68x_restore_setup = const(0x02)



GY68x_header_frame = const(0x5A)

GY68x_altitude_data = const(0x20)
GY68x_gas_data = const(0x10)
GY68x_IAQ_data = const(0x08)
GY68x_air_pressure_data = const(0x04)
GY68x_RH_data = const(0x02)
GY68x_temperature_data = const(0x01)

GY68x_default_packet_size = const(0x0F)


GY68x_data_header_1_frame_positon = const(0)
GY68x_data_header_2_frame_positon = const(1)
GY68x_output_indicator_frame_positon = const(2)
GY68x_packet_size_frame_positon = const(3)
GY68x_temperature_byte_1_frame_positon = const(4)
GY68x_temperature_byte_2_frame_positon = const(5)
GY68x_RH_byte_1_frame_positon = const(6)
GY68x_RH_byte_2_frame_positon = const(7)
GY68x_air_pressure_byte_1_frame_positon = const(8)
GY68x_air_pressure_byte_2_frame_positon = const(9)
GY68x_air_pressure_byte_3_frame_positon = const(10)
GY68x_IAQ_byte_1_frame_positon = const(11)
GY68x_IAQ_byte_2_frame_positon = const(12)
GY68x_gas_byte_1_frame_positon = const(13)
GY68x_gas_byte_2_frame_positon = const(14)
GY68x_gas_byte_3_frame_positon = const(15)
GY68x_gas_byte_4_frame_positon = const(16)
GY68x_altitude_byte_1_frame_positon = const(17)
GY68x_altitude_byte_2_frame_positon = const(18)
GY68x_CRC_frame_positon = const(19)


class GY68x():
    def __init__(self, _uart):
        self.tx_data_frame = bytearray(GY68x_TX_data_packet_size)
        self.rx_data_frame = bytearray(GY68x_RX_data_packet_size)
        
        self.t = 0
        self.p = 0
        self.rh = 0
        self.alt = 0
        self.iaq = 0
        self.gas = 0
        
        self.t_min = -40
        self.t_max = 85
        self.rh_min = 0
        self.rh_max = 100
        self.p_min = 300
        self.p_max = 1100
        self.iaq_min = 0
        self.iaq_max = 500
        self.alt_min = 0
        self.alt_max = 20000
        self.gas_min = 0
        self.gas_max = 16780
        
        self.uart = _uart
        
        
    def send_data(self, cmd, value):
        self.tx_data_frame[0x00] = 0xA5
        self.tx_data_frame[0x01] = cmd
        self.tx_data_frame[0x02] = value
        self.tx_data_frame[0x03] = ((0xA5 + cmd + value) & 0xFF) 
        
        self.uart.write(self.tx_data_frame)
        sleep_ms(10)
        
        
    def set_output_mode(self, mode):
        self.send_data(GY68x_data_output_cmd, mode)
        
        
    def set_baud_rate(self, baud):
        self.send_data(GY68x_baud_rate_cmd, baud)
        
    
    def save_restore_setup(self, mode):
        self.send_data(GY68x_save_restore_setup_cmd, mode)
        
        
    def request_sensor_data(self, req):
        self.send_data(GY68x_data_request_cmd, req)
        
        
    def get_data(self):
        t_current = 0
        p_current = 0
        rh_current = 0
        alt_current = 0
        iaq_current = 0
        gas_current = 0          
        crc = 0
        
        container = (GY68x_altitude_data |
                    GY68x_gas_data |
                    GY68x_IAQ_data |
                    GY68x_air_pressure_data |
                    GY68x_RH_data |
                    GY68x_temperature_data)
           
        
        if(self.uart.any() > 0x00):
            self.rx_data_frame = self.uart.read(GY68x_RX_buffer_size)
            
            if(self.rx_data_frame[GY68x_data_header_1_frame_positon] == GY68x_header_frame):
                
                if(self.rx_data_frame[GY68x_data_header_2_frame_positon] == GY68x_header_frame):
                    
                    if(self.rx_data_frame[GY68x_output_indicator_frame_positon] == container):
                        
                        if(self.rx_data_frame[GY68x_packet_size_frame_positon] == GY68x_default_packet_size):
                            
                            for i in range(GY68x_data_header_1_frame_positon, GY68x_CRC_frame_positon):
                                crc += self.rx_data_frame[i]
                            
                            crc &= 0xFF
                            
                            if(crc == self.rx_data_frame[GY68x_CRC_frame_positon]):
                                
                                t_current = ((self.rx_data_frame[GY68x_temperature_byte_1_frame_positon] << 8) +
                                              self.rx_data_frame[GY68x_temperature_byte_2_frame_positon])
                                
                                if(t_current > 32767):
                                    t_current -= 65536
                                    
                                t_current /= 100.0
                                
                                rh_current = (((self.rx_data_frame[GY68x_RH_byte_1_frame_positon] << 8) +
                                                self.rx_data_frame[GY68x_RH_byte_2_frame_positon]) / 100.0)
                                
                                p_current = ((self.rx_data_frame[GY68x_air_pressure_byte_1_frame_positon] << 16) +
                                             (self.rx_data_frame[GY68x_air_pressure_byte_2_frame_positon] << 8) +
                                              self.rx_data_frame[GY68x_air_pressure_byte_3_frame_positon])
                                
                                p_current /= 100.0
                                
                                iaq_current = (((self.rx_data_frame[GY68x_IAQ_byte_1_frame_positon] & 0x0F) << 8) +
                                                 self.rx_data_frame[GY68x_IAQ_byte_2_frame_positon])
                                
                                gas_current = ((self.rx_data_frame[GY68x_gas_byte_1_frame_positon] << 24) +
                                               (self.rx_data_frame[GY68x_gas_byte_2_frame_positon] << 16) +
                                               (self.rx_data_frame[GY68x_gas_byte_3_frame_positon] << 8) +
                                                self.rx_data_frame[GY68x_gas_byte_4_frame_positon])
                                
                                gas_current /= 1000.0
                                
                                alt_current = (((self.rx_data_frame[GY68x_altitude_byte_1_frame_positon] << 8) +
                                                 self.rx_data_frame[GY68x_altitude_byte_2_frame_positon]))
                                
                                if(alt_current > 32767):
                                    alt_current -= 65536
                                    
                                self.t = t_current
                                self.rh = rh_current
                                self.p = p_current
                                self.iaq = iaq_current
                                self.gas = gas_current
                                self. alt = alt_current
        
        
        return self.t, self.rh, self.p, self.iaq, self.gas, self.alt
