from math import pi

def circle_perimeter(radius):
    if type(radius) not in [int,float]:
        raise TypeError("The radius must be a number")

    if radius < 0:
        raise ValueError("The radius cannot be negative.")

    return pi * 2 * radius


def circle_area(radius):
    if type(radius) not in [int,float]:
        raise TypeError("The radius must be a number")

    if radius < 0:
        raise ValueError("The radius cannot be negative.")

    return pi * (radius**2)


