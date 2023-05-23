from utime import sleep_ms, sleep_us
from micropython import const
import math
import struct


SGP40_I2C_ADDRESS = const(0x59)

SGP40_FEATURE_SET_CMD = [0x20, 0x2F]
SGP40_MEASURE_TEST_CMD = [0x28, 0x0E]
SGP40_SOFT_RESET_CMD = [0x00, 0x06]
SGP40_HEATER_OFF_CMD = [0x36, 0x15]
SGP40_MEASURE_RAW_CMD = [0x26, 0x0F]

CRC_TABLE = [
        0, 49, 98, 83, 196, 245, 166, 151, 185, 136, 219, 234, 125, 76, 31, 46,
        67, 114, 33, 16, 135, 182, 229, 212, 250, 203, 152, 169, 62, 15, 92, 109,
        134, 183, 228, 213, 66, 115, 32, 17, 63, 14, 93, 108, 251, 202, 153, 168,
        197, 244, 167, 150, 1, 48, 99, 82, 124, 77, 30, 47, 184, 137, 218, 235,
        61, 12, 95, 110, 249, 200, 155, 170, 132, 181, 230, 215, 64, 113, 34, 19,
        126, 79, 28, 45, 186, 139, 216, 233, 199, 246, 165, 148, 3, 50, 97, 80,
        187, 138, 217, 232, 127, 78, 29, 44, 2, 51, 96, 81, 198, 247, 164, 149,
        248, 201, 154, 171, 60, 13, 94, 111, 65, 112, 35, 18, 133, 180, 231, 214,
        122, 75, 24, 41, 190, 143, 220, 237, 195, 242, 161, 144, 7, 54, 101, 84,
        57, 8, 91, 106, 253, 204, 159, 174, 128, 177, 226, 211, 68, 117, 38, 23,
        252, 205, 158, 175, 56, 9, 90, 107, 69, 116, 39, 22, 129, 176, 227, 210,
        191, 142, 221, 236, 123, 74, 25, 40, 6, 55, 100, 85, 194, 243, 160, 145,
        71, 118, 37, 20, 131, 178, 225, 208, 254, 207, 156, 173, 58, 11, 88, 105,
        4, 53, 102, 87, 192, 241, 162, 147, 189, 140, 223, 238, 121, 72, 27, 42,
        193, 240, 163, 146, 5, 52, 103, 86, 120, 73, 26, 43, 188, 141, 222, 239,
        130, 179, 224, 209, 70, 119, 36, 21, 59, 10, 89, 104, 255, 206, 157, 172
        ]


WITHOUT_HUM_COMP = [0x26, 0x0F, 0x80, 0x00, 0xA2, 0x66, 0x66, 0x93] 
WITH_HUM_COMP = [0x26, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]


class SGP40():
    def __init__(self, _i2c):
        self.i2c = _i2c
        
        self.write(SGP40_FEATURE_SET_CMD)
        sleep_ms(40)   
        read_buf = self.read() 
        if (((int(read_buf[0]) << 8) | read_buf[1]) != 0x3220):
            raise RuntimeError("SGP40 self test failed!")
        
        self.write(SGP40_MEASURE_TEST_CMD)
        sleep_ms(250)   
        read_buf = self.read() 
        if (((int(read_buf[0]) << 8) | read_buf[1]) != 0xD400):
            raise RuntimeError("SGP40 self test failed!")
        
        
    def read(self):
        retval = self.i2c.readfrom_mem(int(SGP40_I2C_ADDRESS), 0, 3)
        return retval
    
    
    def write(self, cmd):
        self.i2c.writeto_mem(int(SGP40_I2C_ADDRESS), int(cmd[0]), bytes([int(cmd[1])]))
      
      
    def write_block(self, cmd):
        self.i2c.writeto_mem(int(SGP40_I2C_ADDRESS), int(cmd[0]), bytes(cmd[1:8]))
        
        
    def __crc(self, msb, lsb):
        crc = 0xff
        crc ^= msb
        crc = CRC_TABLE[crc]
        if lsb is not None:
            crc ^= lsb
            crc = CRC_TABLE[crc]
        return crc
    
    
    def read_raw(self):
        self.write_block(WITHOUT_HUM_COMP)
        sleep_ms(40)
        read_buf = self.read()
        return ((int(read_buf[0]) << 8) + read_buf[1])
    
    
    def raw_measurement(self, temperature, humidity):
        rh_parameter = struct.pack(">H", math.ceil((humidity * 0xFFFF) / 100))
        rh_crc = self.__crc(rh_parameter[0], rh_parameter[1])

        t_parameter = struct.pack(">H", math.ceil(((temperature + 45) * 0xFFFF) / 175))
        t_crc = self.__crc(t_parameter[0], t_parameter[1])

        WITH_HUM_COMP[2:3] = list(rh_parameter)
        WITH_HUM_COMP[4] = int(rh_crc)
        WITH_HUM_COMP[5:6] = list(t_parameter)
        WITH_HUM_COMP[7] = int(t_crc)

        self.write_block(WITH_HUM_COMP)        
        sleep_ms(60)
        read_buf = self.read()
        return ((int(read_buf[0]) << 8) + read_buf[1])