import argparse
import math

def build_argument_parser():
    """

    Argument parser for a script computing the volume of a cylinder with the option
    of returning as output 3 differently formatted strings.
    
    #### Example
    python 03_test_argparse_mutually_exclusive_group.py -r 10 -H 23
    Cylinder volume is 7225.663103256525

    python 03_test_argparse_mutually_exclusive_group.py -r 10 -H 23 -v
    Cylinder volume of radius=10.0 and height=23.0 is 7225.663103256525

    python 03_test_argparse_mutually_exclusive_group.py -r 10 -H 23 -q
    7225.663103256525

    """
    parser = argparse.ArgumentParser(description="Calculate Cylinder Volume")
    parser.add_argument('-r', '--radius', type=float, metavar='', required=True, help='Radius of the cylinder')
    parser.add_argument('-H', '--height', type=float, metavar='', required=True, help='height of the cylinder')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-q', '--quiet',   action='store_true', help='print quiet, returns a single number')
    group.add_argument('-v', '--verbose', action='store_true', help='print verbose, returns an explanation and numbers')
    args = parser.parse_args()
    return args

def cylinder_volume(radius, height ):
    return math.pi * (radius**2) * height
    
if __name__ == "__main__":
    args = build_argument_parser()

    radius, height = args.radius, args.height
    volume = cylinder_volume(args.radius, args.height)

    if args.quiet:
        print(volume)
    elif args.verbose:
        print("Cylinder volume of radius={} and height={} is {}".format(radius, height, volume))
    else:
        print("Cylinder volume is {}".format(volume))
