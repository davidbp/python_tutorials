# Asyncronous code

**Async is a style of concurrent programming in which tasks release the CPU during waiting periods, so that other tasks can use it.**

The key idea of concurrent programming is to do multiple things at once (as we usually do when we multitasking in our daily live).

A pedantic example might bring some light here. Assume you have to bake a cake and buy some groceries.

- The time needed to bake the cake is 1 hour: 15 minutes are required to prepare the dough and 45 minutes are needed to bake  the cake in the oven.
- The time needed to buy some groceries is 20 minutes.

There are 2 possible solutions for this problem.

- Sincronously: First we make the cake (1 hour) then we go to the grocery store (20 inutes). This solution would need 1 hour and 20 minutes to complete the tasks sequentially.
- Asincronously: First we make the dough of the cake (15 minutes). Then we put the cake into the oven and realease the cake task to go to the grocery store. After 35=(15 + 20) minutes we would have already solved the second task but we would be waiting for the cake to be cooked. 

The previous example is essentially what is shown in  the examples from `test_async.py` and  `test_noasync.py`. 



### How do we tell python to suspend and resume a task

In order to suspend and resume the execution of a function, first we need a special type of function that allows this type of behaviour. These functions in python are defined as  **`async def`** functions. This type of functions have the capability to enter a waiting period which, when it finishes, the function continues running again.

There are different ways to implement functions with the ability to suspend/resume work in Python (without OS interference):

- Callback functions
- Generator functions
- Async/await function



### How do we manage functions that are suspended/resumed in python

Even if we can run functions that have the capability to suspend and resume their work, we need a way to coordinate between the different suspended and resumed functions. This is done by a scheduler, that in this context is called the 'event loop'. 

- The event loop can be created with **event_loop = `asyncio.get_event_loop()`**
- This `event_loop` instance can be used to run a function that can contain multiple calls to other async functions
- To start runing the `event_loop`  the method `event_loop.run_until_complete(f)` has to be called.
- The method `.closed` can be used to wait untill `f` has finished. That is`event_loop.close()` 

The event loop keeps track of all the running tasks.  When a function is suspended, it returns control to the event loop which finds another function to start or resume. This type of behaviour is often called 'cooperative multi-tasking'.



### Multiple processes vs asyncronous code

If you want execute  N tasks in python a possible option is to call N scripts each of which solves a task. This N scripts can be called at the same time in different bash terminals and the execution of one script will not block the others. It is the operating system that will decide how resources are mapped to execute the different scripts. 

- **In CPython the GIL prevents multi-core concurrency**. A python program cannot be using multiple processes at the same time, but the operating system can execute multiple python processes at the same time.

- **Asyncronous python code, as far as the OS in concerned, uses a single process with a single thread.**



#### Example

The code in  `test_async.py` takes around 3 seconds to finish

```
time python3 test_async.py
time passed after iter 0 is 9.5367431640625e-07
time passed after iter 1 is 4.482269287109375e-05
time passed after iter 2 is 5.698204040527344e-05
time passed after iter 3 is 6.604194641113281e-05
time passed after iter 4 is 7.390975952148438e-05

Total time needed was 3.0033140182495117


real	0m3.061s
user	0m0.042s
sys	0m0.013s
```

The code in `test_noasync.py` takes around 15 seconds fo finish

```
time python3 test_noasync.py
time after iter 0 is 1.9073486328125e-06
time after iter 1 is 3.0026869773864746
time after iter 2 is 6.0033111572265625
time after iter 3 is 9.00339412689209
time after iter 4 is 12.00611400604248

Total time needed was 15.011099815368652


real	0m15.044s
user	0m0.021s
sys	0m0.009s
```

Both codes have a function `main` that iterates 5 times calling another function. In the case of the `test_async.py` we can see that the time spend between each time `example_coroutine` is called is very small. 

 In the case of `test_async.py` the function is

```
async def example_coroutine(i):
    time_io_wait = 3
    await asyncio.sleep(time_io_wait)  
```

where as `test_noasync.py` the function is

```

def example_coroutine(i):
    time_io_wait = 3
    time.sleep(time_io_wait) 
```

Note that the first case the function is defined as `async def`.



####  `test_async.py` 

```python
import time
import asyncio
import random

async def example_coroutine(i):
    time_io_wait = 3
    await asyncio.sleep(time_io_wait)   # This simulates waiting some function 
                                        # to recieve info from the internet for example
#    print("example_coroutine {} finished after {} seconds".format(i,time_io_wait))

async def main():
    tasks = []
    t0 = time.time()
    for i in range(5):
        print(f'time passed after iter {i} is {time.time()-t0}')
        tasks.append(asyncio.ensure_future(example_coroutine(i)))

    await asyncio.gather(*tasks)

t0=time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
print("\nTotal time needed was {}\n".format(time.time() -t0 ) )
```







### Async functions calling other async functions

An `async` function `f1` can call another `async` function `f2` as long as `f1` uses the word  `await` before calling `f2`. 

