from micropython import const
from machine import I2C


CONFIG_REG = const(0x00)
SHUNT_VOLTAGE_REG = const(0x01)
BUS_VOLTAGE_REG = const(0x02)
POWER_REG = const(0x03)
CURRENT_REG = const(0x04)
CALIBRATION_REG = const(0x05)


bus_voltage_range_16V = const(0x00)
bus_voltage_range_32V = const(0x01)

gain_div_1_40mV = const(0x00)
gain_div_2_80mV = const(0x01)
gain_div_4_160mV = const(0x02)
gain_div_8_320mV = const(0x03)

ADC_9_bit_1_sample = const(0x00)
ADC_10_bit_1_sample = const(0x01)
ADC_11_bit_1_sample = const(0x02)
ADC_12_bit_1_sample = const(0x03)
ADC_12_bit_2_samples = const(0x09)
ADC_12_bit_4_samples = const(0x0A)
ADC_12_bit_8_samples = const(0x0B)
ADC_12_bit_16_samples = const(0x0C)
ADC_12_bit_32_samples = const(0x0D)
ADC_12_bit_64_samples = const(0x0E)
ADC_12_bit_128_samples = const(0x0F)

power_down_mode = const(0x00)
shunt_voltage_triggered_mode = const(0x01)
bus_voltage_triggered_mode = const(0x02)
shunt_and_bus_voltage_triggered_mode = const(0x03)
adc_off_mode = const(0x04)
shunt_voltage_continuous_mode = const(0x05)
bus_voltage_continuous_mode = const(0x06)
shunt_and_bus_voltage_continuous_mode = const(0x07)


class INA219():

    def __init__(self, _i2c, _i2c_addr, _shunt, _batt_low, _batt_full):
        self.i2c = _i2c
        self.i2c_addr = _i2c_addr
        self.batt_low = _batt_low
        self.batt_full = _batt_full
        self.current_lsb = 0  
        self.calibration_value = 0
        self.power_lsb = 0
        self.shunt_resistor_ohms = _shunt
        self.calibrate_for_32V_2A()


    def read(self, reg):
        value = self.i2c.readfrom_mem(self.i2c_addr, reg, 0x02)
        retval = ((value[0x00] << 0x08) + value[0x01])
        return retval


    def write(self, reg, value):
        if not type(value) is bytearray:
            value = bytearray([value])
        
        self.i2c.writeto_mem(self.i2c_addr, reg, value)
        

    def calibrate_for_32V_2A(self):
        self.current_lsb = 1.0  
        self.power_lsb = 0.002
        self.calibration_value = 4096
        
        configuration = (bus_voltage_range_32V << 13) | \
                        (gain_div_8_320mV << 11) | \
                        (ADC_12_bit_32_samples << 7) | \
                        (ADC_12_bit_32_samples << 3) | \
                        (shunt_and_bus_voltage_continuous_mode)
       
        self.write(CALIBRATION_REG, self.calibration_value)
        self.write(CONFIG_REG, configuration)

        
    def get_shunt_voltage_in_mV(self):
        value = self.read(SHUNT_VOLTAGE_REG)
        
        if(value > 32767):
            value -= 65535

        return (value * 0.01)
        

    def get_bus_voltage_in_mV(self):  
        self.read(BUS_VOLTAGE_REG)
        
        return ((self.read(BUS_VOLTAGE_REG) >> 3) * 0.004 * 1000.0)
        

    def get_current_mA(self):
        value = self.read(CURRENT_REG)
        
        if(value > 32767):
            value -= 65535
        
        return (value * self.current_lsb)
    
    
    def get_current_from_shunt(self):
        value = (self.get_shunt_voltage_in_mV() * 10)
                
        return (value / self.shunt_resistor_ohms)


    def get_power(self):
        value = self.read(POWER_REG)
        
        if(value > 32767):
            value -= 65535
        
        return (value * self.power_lsb * 10.0)
    
    
    def calculate_power(self):
        value = (self.get_current_from_shunt() * self.get_bus_voltage_in_mV())
                
        return (value / 1000000.0)
    
    
    def get_battery_capacity(self):
        capacity = ((((self.get_bus_voltage_in_mV() / 1000.0) - self.batt_low) / (self.batt_full - self.batt_low)) * 100.0)
        
        if(capacity >= 100):
            capacity = 100
        
        if(capacity <= 0):
            capacity = 0
        
        return capacity 
