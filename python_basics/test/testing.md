
# Testing python code

In order to make a test for the code inside  `myfile.py`  we create a file `test_myfile.py`.
Inside `test_myfile.py` we will write the different tests for the methods found in `myfile.py`.

In order to create a test for a function `my_function` we create a class `TestMyFunction(unittest.TestCase)`
which will contain inside different functions that will test different aspects about `my_function`.

For example, the following test class named `TestCircleArea` should test `circle_area`.
Inside the class we have two types of tests. 

- `def test_area(self)` tests if the results of the function are correct. That is, for different inputs, we should know the output
   and check if they match.

- `def test_values(self)` tests if the values provided as input raise the appropiate error when they are outside
  the domain of the function.


```
class TestCircleArea(unittest.TestCase):
    def test_area(self):
        # test areas
        self.assertAlmostEqual(circle_area(1), pi)
        self.assertAlmostEqual(circle_area(2.1), pi*2.1**2)
        self.assertAlmostEqual(circle_area(0), 0)
         
    def test_values(self):
        # Make sure errors are raised when necessary
        self.assertRaises(ValueError, circle_area, -2)
```



## Running test check

In order to run the tests, run in the terminal

```
python -m unittest test_circles.py
```

This should print the results of the tests


## Docstrings

#### Docstrings basics

There is an alternative/additional way to make tests. Python tests can be done in the documentation of functions (inside the sting).
To do this you need to add 

```
>>> myfunction(value)
output
``` 

For example, for a function that doubles a number we would have:
```
>>> double(5)
10
``` 

#### Make a python script execute docstrings

In order to run all the doctests from a file  `my_file.py` you would run

```
python my_file.py -v
```

**You need inside the file   `my_file.py`**  the following code:
```

if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

This code tells python to check the doctest (allways not in the event of `-v`). 
Moreover, if called with `-v` it will print the results of the tests. This means that if a tests fails 
it is displayed even if you do not run the scirpt with `-v`, but if all tests are passed nothing will
be printed unless you call the file explicitly with `-v`.


There is an alternative way to check doctests without having a main in a file.
You can run 
```
python -m doctest my_file.py  -v
```
to asses if all the doctests are passed.


You can try for example 
```
python -m doctest factorial_withoutmain.py  -v
```


##### Example

Try running `python factorial_wrong.py` without the `-v` and the code will produce:

```
python factorial_wrong.py 
**********************************************************************
File "factorial_wrong.py", line 6, in __main__
Failed example:
    factorial(5)
Expected:
    120
Got:
    0
**********************************************************************
File "factorial_wrong.py", line 13, in __main__.factorial
Failed example:
    [factorial(n) for n in range(6)]
Expected:
    [1, 1, 2, 6, 24, 120]
Got:
    [0, 0, 0, 0, 0, 0]
**********************************************************************
File "factorial_wrong.py", line 15, in __main__.factorial
Failed example:
    factorial(30)
Expected:
    265252859812191058636308480000000
Got:
    0
**********************************************************************
File "factorial_wrong.py", line 27, in __main__.factorial
Failed example:
    factorial(30.0)
Expected:
    265252859812191058636308480000000
Got:
    0
**********************************************************************
2 items had failures:
   1 of   1 in __main__
   3 of   6 in __main__.factorial
***Test Failed*** 4 failures.
```

Nevertheless `python factorial.py `  will not produce anything because the tests in the docstrings do not crush.


Notice that this behaviour happens because `factorial_wrong.py` has the main:

```
if __name__ == "__main__":
    import doctest
    doctest.testmod()
```

If you remove the main this will not happen (no errors will be printed). 


##### Example

The code in `factorial.py` contains some doctests.

If you run
```
python factorial.py -v
```

You should see a bunch of outputs with the different tests.


Notice that `factorial_withoutmain.py` does not have a `doctest.testmod()` call. Therefore 

```
python factorial_withoutmain.py  -v
```

will not print anything.


