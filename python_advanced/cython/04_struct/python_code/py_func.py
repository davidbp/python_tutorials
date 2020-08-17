from random import random
from collections import namedtuple

Rectangle = namedtuple('Rectangle', ['w', 'h'])#, verbose=False)

def check_rectangles(rectangles: list, n_rectangles: int, threshold: float):
    n_out = 0
    for rectangle in rectangles[0:n_rectangles]:
        if rectangle.w * rectangle.h > threshold:
            n_out += 1
    return n_out

def verify_rectangles(N):
    n_rectangles = N
    threshold = 0.25

    rectangles = []
    for i in range(n_rectangles):
        rectangle = Rectangle(random(), random())
        rectangles.append(rectangle)

    n_out = check_rectangles(rectangles, n_rectangles, threshold)
    #print(n_out)
