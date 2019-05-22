import argparse
import math

parser = argparse.ArgumentParser(description="Calculate Cylinder Volume")
parser.add_argument('-r', '--radius', type=float, metavar='', required=True, help='Radius of the cylinder')
parser.add_argument('-H', '--height', type=float, metavar='', required=True, help='height of the cylinder')
args = parser.parse_args()

def cylinder_volume(radius, height ):
    return math.pi * (radius**2) * height
    
if __name__ == "__main__":

    radius, height = args.radius, args.height
    volume = cylinder_volume(args.radius, args.height)
    print("Cylinder volume is {}".format(volume))

