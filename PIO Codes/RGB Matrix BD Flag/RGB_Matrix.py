from micropython import const
from machine import Pin
from rp2 import asm_pio, StateMachine, PIO
import array


row = const(10)
col = const(16)
channels = const(3)
colour_depth = const(8)
Total_Bits = (channels * colour_depth)
LEDs = (col * row)


font = [
        [0x00, 0x00, 0x00],                        # Code for char
        [0x00, 0x0B, 0x00],                        # Code for char !
        [0x03, 0x00, 0x03],                        # Code for char "
        [0x1F, 0x0A, 0x1F],                        # Code for char #
        [0x17, 0x1F, 0x1D],                        # Code for char $
        [0x09, 0x04, 0x12],                        # Code for char %
        [0x1A, 0x15, 0x18],                        # Code for char &
        [0x01, 0x06, 0x00],                        # Code for char '
        [0x0E, 0x11, 0x00],                        # Code for char (
        [0x00, 0x11, 0x0E],                        # Code for char )
        [0x14, 0x0E, 0x14],                        # Code for char *
        [0x04, 0x0E, 0x04],                        # Code for char +
        [0x00, 0x04, 0x18],                        # Code for char ,
        [0x04, 0x04, 0x04],                        # Code for char -
        [0x00, 0x08, 0x00],                        # Code for char .
        [0x18, 0x04, 0x03],                        # Code for char /
        [0x1F, 0x11, 0x1F],                        # Code for char 0
        [0x00, 0x1F, 0x00],                        # Code for char 1
        [0x1D, 0x15, 0x17],                        # Code for char 2
        [0x15, 0x15, 0x1F],                        # Code for char 3
        [0x07, 0x04, 0x1F],                        # Code for char 4
        [0x17, 0x15, 0x1D],                        # Code for char 5
        [0x1F, 0x15, 0x1D],                        # Code for char 6
        [0x01, 0x01, 0x1F],                        # Code for char 7
        [0x1F, 0x15, 0x1F],                        # Code for char 8
        [0x17, 0x15, 0x1F],                        # Code for char 9
        [0x00, 0x0A, 0x00],                        # Code for char :
        [0x00, 0x05, 0x18],                        # Code for char ;
        [0x04, 0x0A, 0x11],                        # Code for char <
        [0x0A, 0x0A, 0x0A],                        # Code for char =
        [0x11, 0x0A, 0x04],                        # Code for char >
        [0x03, 0x19, 0x07],                        # Code for char ?
        [0x1F, 0x1D, 0x17],                        # Code for char @
        [0x1E, 0x05, 0x1E],                        # Code for char A
        [0x1F, 0x15, 0x0E],                        # Code for char B
        [0x0E, 0x11, 0x0A],                        # Code for char C
        [0x1F, 0x11, 0x0E],                        # Code for char D
        [0x1F, 0x15, 0x11],                        # Code for char E
        [0x1F, 0x05, 0x01],                        # Code for char F
        [0x0E, 0x11, 0x0D],                        # Code for char G
        [0x1F, 0x04, 0x1F],                        # Code for char H
        [0x11, 0x1F, 0x11],                        # Code for char I
        [0x08, 0x11, 0x0F],                        # Code for char J
        [0x1F, 0x0C, 0x12],                        # Code for char K
        [0x1F, 0x10, 0x10],                        # Code for char L
        [0x1F, 0x02, 0x1F],                        # Code for char M
        [0x1F, 0x01, 0x1F],                        # Code for char N
        [0x0E, 0x11, 0x0E],                        # Code for char O
        [0x1F, 0x05, 0x06],                        # Code for char P
        [0x1F, 0x17, 0x08],                        # Code for char Q
        [0x1F, 0x05, 0x1A],                        # Code for char R
        [0x12, 0x15, 0x09],                        # Code for char S
        [0x01, 0x1F, 0x01],                        # Code for char T
        [0x1F, 0x10, 0x1F],                        # Code for char U
        [0x0F, 0x10, 0x0F],                        # Code for char V
        [0x1F, 0x08, 0x1F],                        # Code for char W
        [0x1B, 0x04, 0x1B],                        # Code for char X
        [0x03, 0x1C, 0x03],                        # Code for char Y
        [0x19, 0x15, 0x13],                        # Code for char Z
        [0x1F, 0x11, 0x00],                        # Code for char [
        [0x02, 0x04, 0x08],                        # Code for char BackSlash
        [0x00, 0x11, 0x1F],                        # Code for char ]
        [0x06, 0x01, 0x06],                        # Code for char ^
        [0x08, 0x08, 0x08],                        # Code for char _
        [0x01, 0x02, 0x00],                        # Code for char `
        [0x0A, 0x15, 0x1E],                        # Code for char a
        [0x1F, 0x14, 0x08],                        # Code for char b
        [0x1E, 0x12, 0x12],                        # Code for char c
        [0x1C, 0x14, 0x1F],                        # Code for char d
        [0x1F, 0x15, 0x17],                        # Code for char e
        [0x1E, 0x05, 0x01],                        # Code for char f
        [0x07, 0x15, 0x1F],                        # Code for char g
        [0x1F, 0x04, 0x1C],                        # Code for char h
        [0x00, 0x1D, 0x00],                        # Code for char i
        [0x10, 0x1D, 0x00],                        # Code for char j
        [0x1E, 0x08, 0x14],                        # Code for char k
        [0x00, 0x1E, 0x10],                        # Code for char l
        [0x1E, 0x04, 0x1E],                        # Code for char m
        [0x1E, 0x02, 0x1E],                        # Code for char n
        [0x1E, 0x12, 0x1E],                        # Code for char o
        [0x1F, 0x05, 0x02],                        # Code for char p
        [0x02, 0x05, 0x1F],                        # Code for char q
        [0x1C, 0x02, 0x02],                        # Code for char r
        [0x16, 0x15, 0x0D],                        # Code for char s
        [0x02, 0x1F, 0x12],                        # Code for char t
        [0x1E, 0x10, 0x1E],                        # Code for char u
        [0x0E, 0x10, 0x0E],                        # Code for char v
        [0x1E, 0x08, 0x1E],                        # Code for char w
        [0x12, 0x0C, 0x12],                        # Code for char x
        [0x16, 0x14, 0x1E],                        # Code for char y
        [0x1D, 0x15, 0x12],                        # Code for char z
        [0x04, 0x1B, 0x11],                        # Code for char {
        [0x10, 0x1F, 0x10],                        # Code for char |
        [0x11, 0x1B, 0x04],                        # Code for char }
        [0x02, 0x04, 0x04],                        # Code for char ~
        [0x0E, 0x09, 0x0E],                         # Code for char 
    ]


class RGB_Matrix():
    
    @asm_pio(sideset_init = PIO.OUT_LOW,
             out_shiftdir = PIO.SHIFT_LEFT,
             autopull = True,
             pull_thresh = Total_Bits)
    
    def WS281x():
        wrap_target()
        label("bitloop")
        out(x, 1)               .side(0)    [2]
        jmp(not_x, "do_zero")   .side(1)    [1]
        jmp("bitloop")          .side(1)    [4]
        label("do_zero")
        nop()                   .side(0)    [4]
        wrap()
        
        
    def __init__(self, _pin, no_of_LEDs = LEDs):
        self.pin = _pin
        self.leds = no_of_LEDs
        
        self.NO = False
        self.YES = True
        
        self.OFF = False
        self.ON = True
        
        self.ROUNDED = False
        self.SQUARE = True
        
        self.BLACK = (0, 0, 0)
        self.RED = (15, 0, 0)
        self.YELLOW = (15, 15, 0)
        self.GREEN = (0, 15, 0)
        self.CYAN = (0, 15, 15)
        self.BLUE = (0, 0, 15)
        self.PURPLE = (15, 0, 15)
        self.WHITE = (15, 15, 15)
        
        self.disp_array = array.array("I", [0 for _ in range(self.leds)])
       
        self.sm = StateMachine(0, RGB_Matrix.WS281x, freq = 8000000, sideset_base = Pin(self.pin))
        self.sm.active(1)
        
    
    def pixels_show(self, brightness):
        display_array = array.array("I", [0 for _ in range(self.leds)])
        
        brightness = (brightness / 100)
        
        for i, c in enumerate(self.disp_array):
            
            r = int(((c >> 8) & 0xFF) * brightness)
            g = int(((c >> 16) & 0xFF) * brightness)
            b = int((c & 0xFF) * brightness)
            
            display_array[i] = ((r << 16) + (g << 8) + b)
            
        self.sm.put(display_array, 8)
        

    def pixels_set(self, i, colour):
        self.disp_array[i] = ((colour[1] << 16) + (colour[0] << 8) + colour[2])
        
        
    def draw_pixel(self, x_pos, y_pos, colour):
        temp = ((y_pos << 4) + x_pos)
        self.pixels_set(temp, colour)


    def pixels_fill(self, colour):
        for i in range(len(self.disp_array)):
            self.pixels_set(i, colour)
            
            
    def draw_line(self, x1, y1, x2, y2, colour):
        dx = (x2 - x1)
        dy = (y2 - y1)
        
        if(dy < 0):
            dy = -dy
            step_y = -1
            
        else:
            step_y = 1
            
        if(dx < 0):
            dx = -dx
            step_x = -1
            
        else:
            step_x = 1
            
        dx <<= 1
        dy <<= 1
        
        self.draw_pixel(x1, y1, colour)
        
        if(dx > dy):
            fraction = (dy - (dx >> 1))
            while(x1 != x2):
                if(fraction >= 0):
                    y1 += step_y
                    fraction -= dx
                
                x1 += step_x
                fraction += dy
                
                self.draw_pixel(x1, y1, colour)
                
        else:
            fraction = (dx - (dy >> 1))
            while(y1 != y2):
                if(fraction >= 0):
                    x1 += step_x
                    fraction -= dy
                
                y1 += step_y
                fraction += dx
                
                self.draw_pixel(x1, y1, colour)
                
    
    def draw_V_line(self, x1, y1, y2, colour):
        self.draw_line(x1, y1, x1, y2, colour)
        
        
    def draw_H_line(self, x1, x2, y1, colour):
        self.draw_line(x1, y1, x2, y1, colour)
        
        
    def draw_circle(self, xc, yc, r, f, colour):
       a = 0
       b = r
       p = (1 - b)
       
       while(a <= b):
           if(f == self.YES):
               self.draw_line((xc - a), (yc + b), (xc + a), (yc + b), colour)
               self.draw_line((xc - a), (yc - b), (xc + a), (yc - b), colour)
               self.draw_line((xc - b), (yc + a), (xc + b), (yc + a), colour)
               self.draw_line((xc - b), (yc - a), (xc + b), (yc - a), colour)
               
           else:
               self.draw_pixel((xc + a), (yc + b), colour)
               self.draw_pixel((xc + b), (yc + a), colour)
               self.draw_pixel((xc - a), (yc + b), colour)
               self.draw_pixel((xc - b), (yc + a), colour)
               self.draw_pixel((xc + b), (yc - a), colour)
               self.draw_pixel((xc + a), (yc - b), colour)
               self.draw_pixel((xc - a), (yc - b), colour)
               self.draw_pixel((xc - b), (yc - a), colour)
            
           if(p < 0):
               p += (3 + (2 * a))
               a += 1
            
           else:
               p += (5 + (2 * (a  - b)))
               a += 1
               b -= 1
               
    def draw_triangle(self, x1, y1, x2, y2, x3, y3, f, colour):
        a = 0
        b = 0
        l = 0
        sa = 0
        sb = 0
        yp = 0
        dx12 = 0
        dx23 = 0
        dx13 = 0
        dy12 = 0
        dy23 = 0
        dy13 = 0
        
        if(f == self.YES):
            if(y1 > y2):
                y1, y2 = y2, y1
                x1, x2 = x2, x1
                
            if(y2 > y3):
                y2, y3 = y3, y2
                x2, x3 = x3, x2
                
            if(y3 > y1):
                y1, y3 = y3, y1
                x1, x3 = x3, x1
                
            if(y1 == y3):
                a = x1
                b = a
                
                if(x2 < a):
                    a = x2
                
                elif(x2 > b):
                    b = x2
                    
                if(x3 < a):
                    a = x3
                
                elif(x3 > b):
                    b = x3
                
                self.draw_H_line(a, (a + (b - (a + 1))), y1, colour)
                return
            
            dx12 = (x2 - x1)
            dy12 = (y2 - y1)
            dx13 = (x3 - x1)
            dy13 = (y3 - y1)
            dx23 = (x3 - x2)
            dy23 = (y3 - y2)
            
            if(y2 == y3):
                l = (y2 + 1)
            
            else:
                l = y2
            
            for yp in range(y1, l):
                a = int(float(x1)+ float(sa / dy12))
                b = int(float(x1) + float(sb / dy13))
                
                sa += dx12
                sb += dx13
                
                if(a > b):
                    a, b = b, a
                
                self.draw_H_line(a, (a + (b - (a + 1))), yp, colour)
            
            sa = int(float(dx23) * float(yp - y2))
            sb = int(float(dx13) * float(yp - y1))

            while(yp <= y3):
                a = int(float(x2) + float(sa / dy23))
                b = int(float(x1) + float(sb / dy13))
                sa += dx23
                sb += dx13

                if(a > b):
                    a, b = b, a
                    
                self.draw_H_line(a, (a + (b - (a + 1))), yp, colour)
                yp += 1
            
        else:
            self.draw_line(x1, y1, x2, y2, colour)
            self.draw_line(x2, y2, x3, y3, colour)
            self.draw_line(x1, y1, x3, y3, colour)
            
    
    def draw_rectangle(self, x1, y1, x2, y2, f, type, colour, back_colour):       
        if(f == self.YES):
            
            if(x1 < x2):
                xmin = x1
                xmax = x2
            
            else:
                xmin = x2
                xmax = x1
                
            if(y1 < y2):
                ymin = y1
                ymax = y2
            
            else:
                ymin = y2
                ymax = y1
                
            while(xmin <= xmax):
                i = ymin
                while(i <= ymax):
                    self.draw_pixel(xmin, i, colour)
                    i += 1
                xmin += 1
                
        else:
            self.draw_V_line(x1, y1, y2, colour)
            self.draw_V_line(x2, y1, y2, colour)
            self.draw_H_line(x1, x2, y1, colour)
            self.draw_H_line(x1, x2, y2, colour)
    
        if(type == self.ROUNDED):
            self.draw_pixel(x1, y1, back_colour)
            self.draw_pixel(x1, y2, back_colour)
            self.draw_pixel(x2, y1, back_colour)
            self.draw_pixel(x2, y2, back_colour)
            
            
    def draw_font(self, x_pos, y_pos, ch, colour, back_colour):        
        v = (ord(ch) - 0x20)
        
        for i in range (0, 3):
            temp = font[v][i]
            for j in range (5, 0, -1):
                if(temp & 0x10):
                   self.draw_pixel((x_pos + i), (y_pos + j), colour)
                else:
                    self.draw_pixel((x_pos + i), (y_pos + j), back_colour)
                
                temp <<= 1
    
    
    def print_str(self, x_pos, y_pos, ch_str, colour, back_colour):
        for chr in ch_str:
            self.draw_font(x_pos, y_pos, chr, colour, back_colour)
            x_pos += 4              
                
