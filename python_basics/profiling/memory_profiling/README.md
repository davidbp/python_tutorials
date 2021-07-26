# Memory Profiling in Python

The package [memory_profiler](https://pypi.org/project/memory-profiler/) can be used to inspect the memory usage of our python code line by line.


To install:

```bash
pip install memory_profiler
```

### Example: `ex_1.py`

The code in `ex_1.py` contains the following:

```python
@profile
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

if __name__ == '__main__':
    my_func()
```

Note that

- `@profile` is written in the function that we want to benchmark.

To benchmark how `ex_1.py` uses memory we can run

```bash
python -m memory_profiler ex_1.py 
```

Will produce

```bash
Filename: ex_1.py

Line #    Mem usage    Increment  Occurences   Line Contents
============================================================
     1   38.461 MiB   38.461 MiB           1   @profile
     2                                         def my_func():
     3   46.094 MiB    7.633 MiB           1       a = [1] * (10 ** 6)
     4  198.684 MiB  152.590 MiB           1       b = [2] * (2 * 10 ** 7)
     5   46.094 MiB -152.590 MiB           1       del b
     6   46.094 MiB    0.000 MiB           1       return a
```



##### Plotting memory usage over time of a Python script

We can run 

```bash
mprof run ex_1.py
```

This will generate a `mprofile_id.dat`  file where `id` will be a long integer number. 

We can generate a plot `mem1.png` of memory usage over time from the `.dat` file as follows:

```bash
mprof plot mprofile_20210726125924.dat -o ./images/mem1.png
```

This will generate the following plot:

![mem1](/Users/davidbuchaca/Documents/git_stuff/python_tutorials/python_basics/profiling/memory_profiling/images/mem1.png)

