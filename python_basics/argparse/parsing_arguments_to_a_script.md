



## How to get the input arguments of a Python script inside python

In Python you can retrieve arguments of an script using the `sys` module.
Arguments are stored in `sys.argv[1:]`, the first argument `sys.argv[0]` is always
the name of the script.



##### Example `01_test_sys_argv.py`

Let us consider  the following code found in `python_basics/sys/01_test_sys_argv.py`

```python
import sys

if __name__ == "__main__":

	print ('Number of arguments:', len(sys.argv), 'arguments.')
	print ('Argument List:', str(sys.argv))
```

This code uses `sys.argv` in order to retrieve the bash commands passed after calling `test_sys_argv.py`. For example if you run `python test_sys_argv.py dog cat` you will get the following:

```bash
python 01_test_sys_argv.py dog cat
```

```bash
Number of arguments: 3 arguments.
Argument List: ['test_sys.py', 'dog', 'cat']
```

Notice that `sys.argv` is a list. You can use the strings inside this list to define different execution branches inside your python script. 



## How to get keyword arguments of a Python script inside python

The module `argparse` from the Python Standard Library allows us to easily write command-line interfaces. To do so, we can define the arguments we expect will be passed when calling a python program. The arguments can be defined as key-word arguments. 

​	args = build_argument_parser()

##### Basic receipt to define a command-line interface with argparse.ArgumentParse

- Define `parser = argparse.ArgumentParser(description="High level program description")`

- Use `parser.add_argument` to add a new command-line keyword argument. 
  - You can add as many keyword arguments as you want.
  - The first argument of `parser.add_argument`  is usually used to define a short version of the name of the key in the keyword argument. By convention, short version arguments have a `-`  followed by a single letter.  For example `-r`.
  - The first argument of `parser.add_argument` defines a  long version of the name of the key in the keyword argument.   By convention, long version arguments have a `--`  followed by a word . For example `--radius`
  - Arguments can be forced using  `required=True` .
  - A help string can be passed to give some information to user 
    - `help="what the keyword argument does"`
  - The type of the keyword argument can be passed with  `type=mytype`, 
    - For example `type=float` or `type=int`.
  
- After all keyword arguments are added an `args` object can be created using `args = parser.parse_args()`. This object will contain the different arguments as variables or fields. The name of the variables will be the name given by the long argument.

  

##### Example `02_test_argparse.py`

Let us make a program that computes the volume of a circle. We want to allow users to pass in the shell the radius an the height of the cylinder. To do so,  we can use `argpase` : 

```python
import argparse
import math

def build_argument_parser():
    parser = argparse.ArgumentParser(description="Calculate Cylinder Volume")
    parser.add_argument('-r', '--radius', type=float, metavar='', required=True, help='Radius of the cylinder')
    parser.add_argument('-H', '--height', type=float, metavar='', required=True, help='height of the cylinder')
    args = parser.parse_args()
    return args

def cylinder_volume(radius, height ):
    return math.pi * (radius**2) * height
    
if __name__ == "__main__":
    radius, height = args.radius, args.height
    volume = cylinder_volume(args.radius, args.height)
    print("Cylinder volume is {}".format(volume))
```

Since the arguments are set with `require=True` notice that the code cannot be called without them:

```bash
python 02_test_argparse.py
```

````bash
usage: 02_test_argparse.py [-h] -r  -H
test_argparse.py: error: the following arguments are required: -r/--radius, -H/--height
````

You can also notice that a useful message is generated telling the user what arguments are needed and the format  required to  pass such information. Example of a correct command line call to our program:

```bash
python 02_test_argparse.py -r 1 -H 1
```

```bash
Cylinder volume is 3.141592653589793
```





## Be careful with boolean command line arguments

The following examples show how you should deal with boolean input times in your command line interface.

##### Example `03_problematic_bool.py`

This example shows that input argument bools are not correctly understood by argparse if you pass them as "True" or "False".

```python
import argparse

def parse_commandline():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('-n', '--name', type=str,   required=True,  help='Person name')
    parser.add_argument('-a',  '--age', type=int,   required=False,  help='Age of the person.')
    parser.add_argument( '-ec', '--ever_convicted',    type=bool,  required=False,  help='Boolean stating if the person has been convicted previously.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":  
    exp_args = parse_commandline()
    print("\tPerson name:", exp_args.name)
    print("\tAge:", exp_args.age)
    print("\tConvicted:", exp_args.ever_convicted)
```

Notice that this program does not behave as you might expect when using "False"

```bash
python 03_problematic_bool.py -n David -a 20 -ec False  
```

	    Person name: David
	    Age: 20
	    Convicted: True
```bash
python 03_problematic_bool.py -n David -a 20 -ec True  
```

        Person name: David
        Age: 20
        Convicted: True


##### Example `04_casting_bool.py`

This example shows how can you use a custom method to solve the issue found in `03_problematic_bool.py`

```python
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def parse_commandline():
    parser = argparse.ArgumentParser(description="Parse inputs")
    parser.add_argument('-n', '--name', type=str,   required=True,  help='Person name')
    parser.add_argument('-a',  '--age', type=int,   required=False,  help='Age of the person.')
    parser.add_argument( '-ec', '--ever_convicted',    type=str2bool,  required=False,  help='Boolean stating if the person has been convicted previously.')
    args = parser.parse_args()
    return args

if __name__ == "__main__":  
    exp_args = parse_commandline()
    print("\tPerson name:", exp_args.name)
    print("\tAge:", exp_args.age)
    print("\tConvicted:", exp_args.ever_convicted)
```

Now we don't have the problem we observed previously.

```bash
python3 04_casting_bool.py -n David -a 20 -ec False
```

```
	Person name: David
	Age: 20
	Convicted: False
```

```bash
python3 04_casting_bool.py -n David -a 20 -ec True
```

```
	Person name: David
	Age: 20
	Convicted: True
```







## How to create mutually exclusive keyword arguments

Sometimes it is interesting to create different types of arguments.

Some arguments can be **required** while others can be **optional**. Sometimes we want optional arguments to be mutually exclusive. For example, we might want a **verbose** argument to be mutually exclusive to a **quiet** argument.

If **verbose** we want the code to print a long description.

If **quiet** we want the code to simply return a number.

Notice that it does not make sense to want both. We can use a `parser.parser.add_mutually_exclusive_group` to precisely code this logic.



##### Example `05_test_argparse_mutually_exclusive_group.py`

```python
import argparse
import math

def build_argument_parser():
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
```

This example provides behavior changes depending on mutually exclusive arguments:

Standard version:

```bash
python 05_test_argparse_mutually_exclusive_group.py -r 10 -H 23
```

```
Cylinder volume is 7225.663103256525
```

Verbose version:

```bash
python 05_test_argparse_mutually_exclusive_group.py -r 10 -H 23 -v
```

```
Cylinder volume of radius=10.0 and height=23.0 is 7225.663103256525
```

Quiet version:

```bash
python 05_test_argparse_mutually_exclusive_group.py -r 10 -H 23 -q
```

```
7225.663103256525
```



