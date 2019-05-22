import argparse
import math

parser = argparse.ArgumentParser(description="Calculate Cylinder Volume")
parser.add_argument('-r', '--radius', type=float, metavar='', required=True, help='Radius of the cylinder')
parser.add_argument('-H', '--height', type=float, metavar='', required=True, help='height of the cylinder')

group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quiet',   action='store_true', help='print quiet, returns a single number')
group.add_argument('-v', '--verbose', action='store_true', help='print verbose, returns an explanation and numbers')
args = parser.parse_args()


def cylinder_volume(radius, height ):
    return math.pi * (radius**2) * height
    
if __name__ == "__main__":

    radius, height = args.radius, args.height
    volume = cylinder_volume(args.radius, args.height)

    if args.quiet:
        print(volume)
    elif args.verbose:
        print("Cylinder volume of radius={} and height={} is {}".format(radius, height, volume))
    else:
        print("Cylinder volume is {}".format(volume))
