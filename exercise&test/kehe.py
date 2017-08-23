from turtle import *
def draw1(n,l):
    pensize(2)
    if(n ==0):
        forward(l)
    else:
        for angle in (60,-120,60,0):
            draw1(n-1,l/3)
            left(angle)

draw1(5,300)
