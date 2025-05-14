# `01_context_manager_timer`


## How to create a context manager

A context manager is a class that needs to have at least two methods:

- **`__enter__`**: executed when the interpreter enters the context block.


- **`__exit__`**: executed allways either after the last line in the context block OR if an error happens.


### Example: Context manager to print execution time 

Let us create a context manager that tells us the execution time of the code within it.

To make it more useful let us print also a user defined string to faciliate knowing what we are timing, in the event we want to time more than one line in a piece of code. 


```python
import time
from time import sleep

class timer():

    def __init__(self, name = ''):
        self.start = time.time()
        self.name = name

    def __enter__(self):
        pass

    def __exit__(self, *args):
        print(f'time {self.name}  {round(time.time() - self.start,6)} sec')
```

Let us use the context manager to time how long does it take to run `sleep(0.2)`

```python
with timer('par for'):
    sleep(0.2)
```

    time par for  0.205038 sec


Note that the execution time is printed even if there is an error


```python
with timer('non existing file'):
    open("does_not_exists.md", 'r')
```

    time non existing file  0.000449 sec



    ---------------------------------------------------------------------------

    FileNotFoundError                         Traceback (most recent call last)

    Cell In[26], line 2
          1 with timer('non existing file'):
    ----> 2     open("does_not_exists.md", 'r')


    File ~/opt/anaconda3/lib/python3.9/site-packages/IPython/core/interactiveshell.py:284, in _modified_open(file, *args, **kwargs)
        277 if file in {0, 1, 2}:
        278     raise ValueError(
        279         f"IPython won't let you open fd={file} by default "
        280         "as it is likely to crash IPython. If you know what you are doing, "
        281         "you can use builtins' open."
        282     )
    --> 284 return io_open(file, *args, **kwargs)


    FileNotFoundError: [Errno 2] No such file or directory: 'does_not_exists.md'


THere is another way to create such context manager, which is using contextlib.contextmanager


```python
from contextlib import contextmanager
import time

@contextmanager
def timer(name=''):
    start = time.time()
    yield
    end = time.time()
    print(f"Time needed for {name}: {end-start} sec")
```


```python
import requests

with timer('sum'):
    2*3
```

    Time needed for sum: 3.0994415283203125e-06 sec

