# Doctest

A **doctest** is a test that is perfomed in documentation of a function.

To generate a test, code must be written as  `>>> python_code`  where `python_code` represents any valid python code that is expected to be tested. A test must have the expectect output in  a newline. The following example shows a function that prints `hello name` for any `name` provided as input. 

```
def hello_name(name=""):
    """ 
    Prints "hello name" given any input string name.
    If no name is passed, it prints "hello "

    >>> hello_name()
    hello 

    >>> hello_name("David")
    hello David
    """
    print(f"hello {name}")
```

The  command **`pytest --doctest-modules`** verifies all doctests in all the modules (.py files) in a folder.

If we execute the command in `python_tutorials/python_basics/doctest`  this will print 

``` 
 pytest --doctest-modules
==================================================================== test session starts =====================================================================
platform darwin -- Python 3.7.6, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
rootdir: /Users/davidbuchaca1/Documents/git_stuff/python_tutorials/python_basics/doctest
plugins: arraydiff-0.3, openfiles-0.4.0, hypothesis-5.15.1, remotedata-0.3.1, doctestplus-0.6.1, astropy-header-0.1.2
collected 2 items                                                                                                                                            

01_doctest.py .                                                                                                                                        [ 50%]
02_doctest_fail.py F                                                                                                                                   [100%]

========================================================================== FAILURES ==========================================================================
____________________________________________________________ [doctest] 02_doctest_fail.hello_name ____________________________________________________________
002  
003     Prints "hello name" given any input string name.
004     If no name is passed, it prints "hello "
005 
006     >>> hello_name()
007     hello 
008 
009     >>> hello_name("David")
Expected:
    hello Pedro
Got:
    hello David

/Users/davidbuchaca1/Documents/git_stuff/python_tutorials/python_basics/doctest/02_doctest_fail.py:9: DocTestFailure
================================================================== short test summary info ===================================================================
FAILED 02_doctest_fail.py::02_doctest_fail.hello_name
================================================================ 1 failed, 1 passed in 0.03s =================================================================
```

this shows that  `02_doctest_fail.py` fails a doctest. The failure information is shown by an `F` in `02_doctest_fail.py F`. Moreover, the test tells us what it expected and what it recieved.

It also  shows that line `009` contained a `hello_name("David")` that did not pass the test. Therefore, we can check if the code is correct or if the test is incorrect.

