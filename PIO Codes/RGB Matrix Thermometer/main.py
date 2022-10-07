from machine import ADC
from RGB_Matrix import RGB_Matrix
from utime import sleep_ms


conversion_factor = 3300.0 / 65535.0


t = 0
tgl = 0
ws = RGB_Matrix(6)
TMP36 = ADC(1)


def map_value(v, x_min, x_max, y_min, y_max):
    return int(y_min + (((y_max - y_min) / (x_max - x_min)) * (v - x_min)))


def constrain_value(v, max_v, min_v):
    if(v >= max_v):
        v = max_v
    
    if(v <= min_v):
        v = min_v
        
    return v


def adc_avg():
    avg = 0
    for i in range (0, 16):
        avg += TMP36.read_u16()
        
    return (avg >> 4)


def graphical_thermometer(value):
    ws.pixels_fill(ws.BLACK)

    ws.draw_V_line(0, 3, 5, ws.WHITE)
    ws.draw_V_line(1, 2, 6, ws.WHITE)
    ws.draw_V_line(2, 1, 7, ws.WHITE)
    ws.draw_V_line(3, 1, 7, ws.WHITE)
    ws.draw_V_line(4, 2, 6, ws.WHITE)
    ws.draw_H_line(5, 14, 3, ws.WHITE)
    ws.draw_H_line(5, 14, 5, ws.WHITE)
    ws.draw_pixel(15, 4, ws.WHITE)

    for i in range(5, 15, 2):
        ws.draw_V_line((i + 1), 7, 8, ws.BLUE)
        ws.draw_V_line(i, 7, 7, ws.GREEN)

        
    ws.draw_V_line(1, 3, 5, ws.RED)
    ws.draw_V_line(1, 3, 5, ws.RED)
    ws.draw_V_line(1, 3, 5, ws.RED)
    ws.draw_V_line(2, 2, 6, ws.RED)
    ws.draw_V_line(3, 2, 6, ws.RED)
    ws.draw_V_line(4, 3, 5, ws.RED)

    bar = map_value(value, 0, 50, 5, 14)
    bar = constrain_value(bar, 14, 5)
    
    ws.draw_H_line(5, bar, 4, ws.RED)

    
def numerical_thermometer(value):
    ws.pixels_fill(ws.BLACK)
    ws.print_str(0, 2, (str("%s" %value) + "C"), (24, 9, 36), ws.BLACK)
    

while(True):
    tmp = conversion_factor * adc_avg()
    t = int(tmp / 28.0)
    
    tgl = (tgl ^ 1)
    
    if(tgl == 0):
        numerical_thermometer(t)
    else:
        graphical_thermometer(t)
        
    ws.pixels_show(25)
    sleep_ms(3000)
        