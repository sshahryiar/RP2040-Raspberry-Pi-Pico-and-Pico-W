from micropython import const
from machine import Pin, I2C
from utime import sleep_ms, sleep_us

#I2C Details
RGB1602_I2C = const(1)
RGB1602_I2C_SDA = Pin(6)
RGB1602_I2C_SCL = Pin(7)

RGB_LCD_I2C = I2C(RGB1602_I2C, sda = RGB1602_I2C_SDA, scl = RGB1602_I2C_SCL, freq = 400000)


#Device I2C Addresses
LCD_I2C_address = const(0x3E)
RGB_I2C_address = const(0x60)

#color define
REG_RED = const(0x04)
REG_GREEN = const(0x03)
REG_BLUE = const(0x02)
REG_MODE_1 = const(0x00)
REG_MODE_2 = const(0x01)
REG_OUTPUT = const(0x08)

LCD_CLEAR_DISPLAY = const(0x01)
LCD_RETURN_HOME = const(0x02)
LCD_ENTRY_MODE_SET = const(0x04)
LCD_DISPLAY_CONTROL = const(0x08)
LCD_CURSOR_SHIFT = const(0x10)
LCD_FUNCTION_SET = const(0x20)
LCD_SET_CGRAM_ADDR = const(0x40)
LCD_SET_DDRAM_ADDR = const(0x80)

#flags for display entry mode
LCD_ENTRY_RIGHT = const(0x00)
LCD_ENTRY_LEFT = const(0x02)
LCD_ENTRY_SHIFT_INCREMENT = const(0x01)
LCD_ENTRY_SHIFT_DECREMENT = const(0x00)

#flags for display on/off control
LCD_DISPLAY_ON = const(0x04)
LCD_DISPLAY_OFF = const(0x00)
LCD_CURSOR_ON = const(0x02)
LCD_CURSOR_OFF = const(0x00)
LCD_BLINK_ON = const(0x01)
LCD_BLINK_OFF = const(0x00)

#flags for display/cursor shift
LCD_DISPLAY_MOVE = const(0x08)
LCD_CURSOR_MOVE = const(0x00)
LCD_MOVE_RIGHT = const(0x04)
LCD_MOVE_LEFT = const(0x00)

#flags for function set
LCD_8_BIT_MODE = const(0x10)
LCD_4_BIT_MODE = const(0x00)
LCD_2_LINE = const(0x08)
LCD_1_LINE = const(0x00)
LCD_5x8_DOTS = const(0x00)

#Data / Command selection
DAT = const(0x40)
CMD = const(0x80)


class RGB1602:
  def __init__(self, row, col):
    self._row = row
    self._col = col
    self._showfunction = (LCD_4_BIT_MODE | LCD_1_LINE | LCD_5x8_DOTS)
    self.initialize(self._row, self._col)


  def write(self, value, loc):
    RGB_LCD_I2C.writeto_mem(LCD_I2C_address, loc, chr(value))
    
    
  def set_reg(self, reg, value):
    RGB_LCD_I2C.writeto_mem(RGB_I2C_address, reg, chr(value))


  def set_RGB(self, r, g, b):
    self.set_reg(REG_RED, r)
    self.set_reg(REG_GREEN, g)
    self.set_reg(REG_BLUE, b)


  def goto_xy(self, x_pos, y_pos):
      if(y_pos == 0):
          x_pos |= 0x80
      else:
          x_pos |= 0xC0
      
      RGB_LCD_I2C.writeto(LCD_I2C_address, bytearray([0x80, x_pos]))


  def clear_home(self):
      self.write(LCD_CLEAR_DISPLAY, CMD)
      self.write(LCD_RETURN_HOME, CMD)
      sleep_ms(2) 
    
    
  def put_chr(self, ch):
      self.write(ord(ch), DAT)
        
        
  def put_str(self, ch_str):
      for chr in ch_str:
            self.put_chr(chr)


  def display(self):
    self._showcontrol |= LCD_DISPLAY_ON 
    self.write((LCD_DISPLAY_CONTROL | self._showcontrol), CMD)

 
  def initialize(self, cols, rows):
    if (rows > 1):
        self._showfunction |= LCD_2_LINE 
    
    sleep_ms(50)
    
    #  Send function set command sequence and try 
    self.write((LCD_FUNCTION_SET | self._showfunction), CMD)
    sleep_ms(5)
    
    # Second try
    self.write((LCD_FUNCTION_SET | self._showfunction), CMD)
    sleep_ms(5)
    
    # Third try
    self.write((LCD_FUNCTION_SET | self._showfunction), CMD)
    
    # Finally, set # lines, font size, etc.
    self.write((LCD_FUNCTION_SET | self._showfunction), CMD)
    
    # Turn the display on with no cursor or blinking default
    self._showcontrol = (LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF)
    self.display()
    
    # Clear LCD & goto to home location
    self.clear_home()
    
    # Initialize to default text direction
    self._showmode = (LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)
    
    # Set the entry mode
    self.write((LCD_ENTRY_MODE_SET | self._showmode), CMD)
    
    # Backlight init
    self.set_reg(REG_MODE_1, 0x00)
    
    # Set LEDs controllable by both PWM and GRPPWM registers
    self.set_reg(REG_OUTPUT, 0xFF)
    
    # Set MODE2 values
    # 0010 0000 -> 0x20  (DMBLNK to 1, ie blinky mode)
    self.set_reg(REG_MODE_2, 0x20)
    
    #Set LCD colour to white initially
    self.set_RGB(255, 255, 255)

