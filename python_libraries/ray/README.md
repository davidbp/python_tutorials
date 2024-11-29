

# Introduction to Ray


Ray introduces the `ray.remote` decorator which turns a python function into a "remote function".
Remote functions are "futures", a remote function `f` can runned with `f.remote()`.
This will trigger the execution of the function but not block the runtime of the program (as an async function).

In `01_parallel_calls.py` one can see the execution of a remote function, where each call needs 2 seconds.
The remote function runned 10 times takes approximately 2 seconds, whereas the serial takes around 20.

```
python 01_parallel_calls.py 
```

```
2024-11-29 16:08:09,296	INFO worker.py:1819 -- Started a local Ray instance.

Successfully imported ray!

sum_serial(n)=10
time sum_serial=20.037309885025024

sum_remote(n)=10
time sum_remote=2.1553449630737305
```