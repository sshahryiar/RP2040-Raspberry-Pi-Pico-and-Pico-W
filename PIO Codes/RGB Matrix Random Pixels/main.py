from RGB_Matrix import RGB_Matrix
from utime import sleep_ms
from random import randint, randrange


ws = RGB_Matrix(6)

while(True):
    #ws.pixels_fill(ws.BLACK)
    x_pos = randrange(0, 16)
    y_pos = randrange(0, 10)
    ws.draw_pixel(x_pos, y_pos, (randint(0, 16), randint(0, 16), randint(0, 16)))
    ws.pixels_show(randint(10, 25))
    sleep_ms(40)