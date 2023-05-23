from micropython import const
from struct import unpack_from
from utime import sleep_us,sleep_ms


SHTC3_I2C_ADDRESS = const(0x70)

SHTC3_REG_SLEEP = const(0xB098)
SHTC3_REG_WAKEUP = const(0x3517)
SHTC3_REG_SOFT_RESET = const(0x805D)
SHTC3_REG_READ_ID = const(0xEFC8)

SHTC3_REG_NORMAL_T_F = const(0x7866)
SHTC3_REG_NORMAL_H_F = const(0x58E0)

SHTC3_REG_NORMAL_T_F_STRETCH = const(0x7CA2)
SHTC3_REG_NORMAL_H_F_STRETCH = const(0x5C24)

SHTC3_REG_LOW_POWER_T_F = const(0x609C)
SHTC3_REG_LOW_POWER_H_F = const(0x401A)

SHTC3_REG_LOW_POWER_T_F_STRETCH = const(0x6458)
SHTC3_REG_LOW_POWER_H_F_STRETCH = const(0x44DE)

SHTC3_NORMAL_MEAS = [SHTC3_REG_NORMAL_T_F, SHTC3_REG_NORMAL_H_F]
SHTC3_LOW_POWER_MEAS = [SHTC3_REG_LOW_POWER_T_F, SHTC3_REG_LOW_POWER_H_F]
SHTC3_NORMAL_MEAS_STRETCH = [SHTC3_REG_NORMAL_T_F_STRETCH, SHTC3_REG_NORMAL_H_F_STRETCH]
SHTC3_LOW_POWER_MEAS_STRETCH = [SHTC3_REG_LOW_POWER_T_F_STRETCH, SHTC3_REG_LOW_POWER_H_F_STRETCH]

SHTC3_MEAS = [SHTC3_NORMAL_MEAS, SHTC3_LOW_POWER_MEAS]
SHTC3_MEAS_STRETCH = [SHTC3_NORMAL_MEAS_STRETCH, SHTC3_LOW_POWER_MEAS_STRETCH]
SHTC3_MEAS_ALL = [SHTC3_MEAS, SHTC3_MEAS_STRETCH]


class SHTC3():    
    
    def __init__(self, _i2c):
        self.cmd = bytearray(2)
        self.buffer = bytearray(6)
        self.i2c = _i2c

        self.i2c.writeto(SHTC3_I2C_ADDRESS, bytes([0x00, 0x00, 0x00]))
        print("SHTC3 ID = {:x}".format(self.read_ID()))


    @staticmethod
    def crc8(buffer: bytearray) -> int:
        crc = 0xFF
        for byte in buffer:
            crc ^= byte
            for _ in range(0, 8, 1):
                if(crc & 0x80):
                    crc = ((crc << 1) ^ 0x31)
                else:
                    crc = (crc << 1)
        return (crc & 0xFF) 
    
    
    def write_command(self, command:int):
        self.cmd[1] = (command & 0xFF)
        self.cmd[0] = (command >> 0x08)
        self.i2c.writeto(SHTC3_I2C_ADDRESS, self.cmd)


    def sleep(self):
        self.write_command(SHTC3_REG_SLEEP)
        sleep_us(300)
        
        
    def wakeup(self):
        self.write_command(SHTC3_REG_WAKEUP)
        sleep_us(300)
        
        
    def soft_reset(self):
        self.write_command(SHTC3_REG_SOFT_RESET)
        sleep_us(300)


    def read_ID(self):
        self.write_command(SHTC3_REG_READ_ID)
        self.buffer=self.i2c.readfrom(SHTC3_I2C_ADDRESS, 3)
        id = ((self.buffer[0] << 8) | self.buffer[1])
        
        return id


    def measure(self, low_power_meas = False, clk_stretch = False):
        command = SHTC3_MEAS_ALL[clk_stretch][low_power_meas][False]
        self.write_command(command)
        
        if(low_power_meas == True):
            sleep_ms(2)
        else:
            sleep_ms(14)
            
        self.buffer=self.i2c.readfrom(SHTC3_I2C_ADDRESS, 6)
        temp_data = self.buffer[0:2]
        temp_data_crc = self.buffer[2]
        hum_data = self.buffer[3:5]
        hum_data_crc = self.buffer[5]

        if((temp_data_crc != self.crc8(temp_data)) or (hum_data_crc != self.crc8(hum_data))):
            print("crc error")
            return (0, 0)
        else :
            T_RAW = ((temp_data[0] << 8) | temp_data[1])
            RH_RAW = ((hum_data[0] << 8) | hum_data[1])
            t = ((T_RAW * 175.0) / 65536.0) - 45.0
            rh = ((RH_RAW * 100.0) / 65536.0) 
            return (t, rh)