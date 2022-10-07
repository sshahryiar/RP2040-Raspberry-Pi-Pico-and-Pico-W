from RGB_Matrix import RGB_Matrix
from utime import sleep_ms
from random import randint


tgl = 0
ws = RGB_Matrix(6)

while(True):
    ws.pixels_fill(ws.YELLOW)
    tgl = tgl ^ 1
    for i in range(0, 2):
        for k in range(0, 16, 2):
            if(tgl):
                ws.draw_V_line(k, (1 - i), (8 + i), ws.GREEN)
                ws.draw_V_line((k + 1), (2 - i), (7 + i), ws.GREEN)
            else:
                ws.draw_V_line((k + 1), (1 - i), (8 + i), ws.GREEN)
                ws.draw_V_line(k, (2 - i), (7 + i), ws.GREEN)
            
            
        ws.draw_circle((8 + i), (tgl + 4), 2, True, ws.RED)
        ws.pixels_show(15)
        sleep_ms(randint(50, 300))