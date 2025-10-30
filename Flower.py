from turtle import *
from colorsys import *

bgcolor("black")
speed(0)
h=0

for i in range(200):
    if i % 2 == 0:
        color(hsv_to_rgb(0.0, 1, 1))  # bright red
    else:
        color(hsv_to_rgb(0.55, 0.7, 1))  # nice bright blue

    
    circle(-i*0.68,200)
    right(80)

done()