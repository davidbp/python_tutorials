

## How to get the input arguments of a Python script inside python

In Python you can retrieve arguments of an script using the `sys` module.
Arguments are stored in `sys.argv[1:]`, the first argument `sys.argv[0]` is allways
the name of the script.


For example if you run `python test_sys.py dog cat` you will get the following:

```
python test_sys_argv.py dog cat
Number of arguments: 3 arguments.
Argument List: ['test_sys.py', 'dog', 'cat']
```

Notice that `sys.argv` is a list.

## How to get keyword arguments of a Python script inside python

The module `argparse` from the Python Standard Library allows us to easily write command-line interfaces. We need to define what arguments we require and `argpase` will parse them from `sys.argv`. 

```
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

```

Since the arguments are set with `require=True` notice that the code cannot be called without them:

````
python test_argparse.py
usage: test_argparse.py [-h] -r  -H
test_argparse.py: error: the following arguments are required: -r/--radius, -H/--height
````

You can also notice that argparse generates a useful message telling you what arguments are needed and how you can  pass them as keyword arguments.

```
python test_argparse.py -r 1 -H 1
Cylinder volume is 3.141592653589793
```



## How to create mutaully exclusive keyword arguments

Sometimes it is interesting to create different types of arguments.

Some arguments can be **required** while others can be **optional**. Sometimes we want optional arguments to be mutually exclusive. For example, we might want a **verbose** argument to be mutually exclusive to a **quiet** argument.

If **verbose** we want the code to print a long description

If **quiet** we want the code to simply return a number.

Notice that it does not make sense to want both. We can do this using a group.

```
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
```

Notice that the behaviour changes in the following 3 cases:

```
python test_argparse_extended.py -r 10 -H 23
Cylinder volume is 7225.663103256525

python test_argparse_extended.py -r 10 -H 23 -v
Cylinder volume of radius=10.0 and height=23.0 is 7225.663103256525

python test_argparse_extended.py -r 10 -H 23 -q
7225.663103256525
```

