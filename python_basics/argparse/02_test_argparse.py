import argparse
import math

def build_argument_parser():
    """
    This function creates an `argparse.Namespace` object named `args` storing 
    the information passed by the command-line interface when calling the script.

        argparse.Namespace: 
        Simple class used by default by parse_args() to create an object holding attributes and return it.
 
    #### Example
    python test_argparse.py -r 12 -H 1
    Cylinder volume is 452.389342117
    """

    parser = argparse.ArgumentParser(description="Calculate Cylinder Volume")
    parser.add_argument('-r', '--radius', type=float, metavar='', required=True, help='Radius of the cylinder')
    parser.add_argument('-H', '--height', type=float, metavar='', required=True, help='height of the cylinder')
    args = parser.parse_args()
    return args

def cylinder_volume(radius, height ):
    return math.pi * (radius**2) * height

if __name__ == "__main__":
    args = build_argument_parser()
    radius, height = agrs.radius, args.height
    
    volume = cylinder_volume(radius, height)
    print("Cylinder volume is {}".format(volume))

