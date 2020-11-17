# Multiprocessing

Before we start with the basics of multiprocessing let us define some of the concepts we need:

- A process is the instance of a computer program that is being executed by one or multiple threads.
- A process is created by the operating system to run a program.
- A process has the capacity to spawn threads (also called sub-processes) to handle subtasks.



#### Main differences between processes and threads

- Processes have more overhead than threads, opening and closing processes takes more time tan opening and closing threads.
- By default the threads spawned in a process share the memory space, and they share it effeiciently.

- - Memory space shared by threads within a process allows threads to write to the same variables
  - This arbitrary access of variables can cause race conditions.
- Two independent processes do not share memory, that is one of the major point of processes.
  - Modern OS allow "shared memory" to be used by multiple processes, but this needs to be explicitly creted.
  - Sharing information between processes is slower than sharing between threads:
    - In python processes share information by pickling data structures such as arrays, this requires IO time.



#### Using Threads or processes?

Well, in python multi-threading is not allowed, so...

- **Processes** speed up Python code that is CPU intensive since they benefit from multiple cores and avoid the GIL.

- **Threads** are best for IO tasks or tasks involving reading and writting to disk (or the internet) because threads can combine their work more efficiently. Processes need to pickle their results to combine them which takes time.



#### Python GIL

GPython, the standard python implementation, has a GIL (Global interpreter Lock) which prevents two threads from executing simultaneously in the same program. One of the main advantages of the GIL is that prevents race conditions in programs, which might cause many bugs in multithreaded workloads.  Neverhteless, this is it's main disadvantage. Since python  does not allow multithreaded code, there can be no bugs introduced by multithreaded code.

To be precise, **the GIL effectively makes any CPU-bound Python program single-threaded**.

Even though Python does not allow multithreaded code to be build from within python, users can write easily code that leverages multithreading, using libraries that run multithreaded code. For example, the following code that executes two matrix operations uses multiple threads.

```python
X1 = np.random.rand(10000,10000)
X2 = np.random.rand(10000,10000)

print(np.matmul(X1,X2)) # here multiple threads can be used because numpy allows it
print(np.matmul(X2,X2)) # here multiple threads can be used because numpy allows it
```

Let us assume we have a machine that can use 4 threads.

We could make a diagram of how the computation fo the previous python snippet would operate:

```
Process 1:
calling numpy 
GIL released
    thread 1 ----------- np.matmul(X1,X2) ---------------
    thread 2 ----------- np.matmul(X1,X2) ---------------
    thread 3 ----------- np.matmul(X1,X2) ---------------
    thread 4 ----------- np.matmul(X1,X2) ---------------
GIL locked

calling numpy 
GIL released
    thread 1 ----------- np.matmul(X2,X2) ---------------
    thread 2 ----------- np.matmul(X2,X2) ---------------
    thread 3 ----------- np.matmul(X2,X2) ---------------
    thread 4 ----------- np.matmul(X2,X2) ---------------
GIL aquired
```



#### Example

Imagine a program that needs to do 2 tasks that are independend and require the same time. Let us see

##### Multi-threading

One possible way to organize the work is use one process and two independent threads 

- Python cannot do this type of paralel programs, nevertheless, there is the `threading` package that allows launching threads.

```
Process 1:
    thread 1 ----------- task 1 ---------------
    thread 2 ----------- task 2 ---------------
```

##### Multi-processing

Another possible way to organize the work is to use 2 processes with a single tread each.

- Python can do this type of paralel programs   using `multiprocessing`.
- Note that in essence, this is no longer one python program, but 2 Python programs that execute two tasks in two using two independent Python interpreters (with one GIL in each process).

```
Process 1:
    thread 1 ----------- task 1 ---------------

Process 2:
    thread 1 ----------- task 2 ---------------
```



## Introduction to `multiprocessing`

The **`multiprocessing`** module allows us to open different threads and do independent computations (at the same time) in different cpu cores.

- **`multiprocessing.Process`**: creates a new process identifier. This can be used to start a task that runs as an independent child process in the operating sstem. 
- **`multiprocessing.Pool`**: creates a pool of workkers that share a chunk of work and return an agretated result.
- **`multiprocessing.Queue`**: A FIFO queue allowing multiple producers and consumers.
- **`multiprocessing.Pipe`**: A uni- or bidirectional communication channel between two processes.
- **`multiprocessing.Manager`**: A high-level managed interface to share Python objects between processes.

The most basic object is the `multiprocessing.Process` obejct:

- **`multiprocessing.Process`** : Process objects represent activity that is run in a separate process
  - `process = Process(target=f,kwargs=f_kwargs))` creates a `Process` object with the function `f` and the input arguments of `f` in `f_kwargs`.
  - `process.start()` starts running `f`  in a separate Python process. The python interpreter does not stop here, it follows executing anything after `process.start()` .
  - `process.join()` waits until the process created by `process.start()` finishes. It is also possible to pass a timeout argument (a float representing the number of seconds to wait). If the process does not complete within the timeout period, `join()` returns anyway.

Let us present an example where we want to execute a function as many times a processes we create. The following code calls the function `sum_up_to_n` as many times as independend CPUs  we have available in our operating system. In this case we have `os.cpu_count()` independend cores where we can launch processes.

```python
import os
import math
from multiprocessing import Process

def sum_up_to_n(process_id,n=50000000):
    aux = 0
    for i in range(0, n):
        aux +=1
    print(f'process {process_id} finished result {aux}')

processes = []
for i in range(os.cpu_count()):
    print(f'starting process {i}')
    processes.append(Process(target=calc,kwargs={'process_id':i}))
    process.start()

for process in processes:
    process.join()
```

The output of the previous code snipet is:

```
starting process 0
starting process 1
starting process 2
starting process 3
starting process 4
starting process 5
starting process 6
starting process 7

process 3 finished result 50000000
process 1 finished result 50000000
process 2 finished result 50000000
process 7 finished result 50000000
process 4 finished result 50000000
process 5 finished result 50000000
process 6 finished result 50000000
process 0 finished result 50000000
```

Note that the processes did not finish in order.

A natural question arises: how can we schedule different tasks into different processes assuming we have more tasks than processes? A possible answer is to use a `multiprocessing.Pool` object that will execute different tasks on the processes created by the pool. 



### Executing in a Pool of processes: `multiprocessing.Pool`

A pool of processes is simply a bunch of processes that can be used to execute a function over a collection.

Let us assume we have a function `func` and a collection `col` and we want to map the function over a collection.

In order words, we want to compute `[f(col[0]), f(col[1]),  f(col[2]), ...]` 

This can be done as follows:

```python
p = Pool()
result = p.map(func, col)
p.close()
p.join()
```

We can also specify the number of processes using `p = Pool(processes=n_processes)` where `n_processes` is the number of processes we allow our Pool to use.



### Mutexes or locks in Multiprocessing: `multiprocessing.Lock` 

Sometimes we might want to spawn multiple processes with the capability to  modify a given shared  object, such as a value or an array. If we do not do this carefully we might get bugs because of race conditions. 

- **`lock = multiprocessing.Lock()`** creates a `Lock` object with the methods `lock.aquire()` and `lock.release()` that allow safe access to any variable between the two calls.

- **`var = multiprocessing.Value('i', init_val) `** creates a variable of type int ( because we specified `i`) with initial value `init_val`

  

  ```python
  import multiprocessing 
    
  # function to withdraw from account 
  def withdraw(balance, lock):     
      for _ in range(10000): 
          lock.acquire() 
          balance.value = balance.value - 1
          lock.release() 
  
  def deposit(balance, lock):     
      for _ in range(10000): 
          lock.acquire() 
          balance.value = balance.value + 1
          lock.release() 
      
  def perform_transactions(): 
    
      # initial balance (in shared memory) 
      balance = multiprocessing.Value('i', 100) 
    
      # creating a lock object 
      lock = multiprocessing.Lock() 
    
      # creating new processes 
      p1 = multiprocessing.Process(target=withdraw, args=(balance,lock)) 
      p2 = multiprocessing.Process(target=deposit, args=(balance,lock)) 
    
      # starting processes 
      p1.start() 
      p2.start() 
    
      # wait until processes are finished 
      p1.join() 
      p2.join() 
    
      # print final balance 
      print("Final balance = {}".format(balance.value)) 
  
      
  for _ in range(10): 
     # perform same transaction process 10 times 
     perform_transactions() 
  ```

```python
import multiprocessing 
  
# function to withdraw from account 
def withdraw(balance):     
    for _ in range(10000): 
        balance.value = balance.value - 1

def deposit(balance):     
    for _ in range(10000): 
        balance.value = balance.value + 1

def perform_transactions(): 
  
    # initial balance (in shared memory) 
    balance = multiprocessing.Value('i', 100) 
  
    # creating new processes 
    p1 = multiprocessing.Process(target=withdraw, args=(balance,)) 
    p2 = multiprocessing.Process(target=deposit, args=(balance,)) 
  
    # starting processes 
    p1.start() 
    p2.start() 
  
    # wait until processes are finished 
    p1.join() 
    p2.join() 
  
    # print final balance 
    print("Final balance = {}".format(balance.value)) 

for _ in range(10): 
    # perform same transaction process 10 times 
    perform_transactions() 
```

The following example will produce a different output almost every time it is executed because there is a race condition. Here different Processes acces the variable `balance` and they change it without coordination. Note that we should have a final balance of 100 every time `perform_transactions` is called, because the function first  uses `withdraw ` to remove `10000` from balance and then calls `deposit` to add `10000` to `balance`. Since the processes are not coordinated they add and substract values at different 'points in time'.

```
Final balance = -2584
Final balance = -2229
Final balance = 2738
Final balance = -686
Final balance = -1674
Final balance = -3161
Final balance = -4893
Final balance = 5750
Final balance = 876
Final balance = 998
```

`lock = multiprocessing.Lock()`

```python
import multiprocessing 
  
# function to withdraw from account 
def withdraw(balance, lock):     
    for _ in range(10000): 
        lock.acquire() 
        balance.value = balance.value - 1
        lock.release() 

def deposit(balance, lock):     
    for _ in range(10000): 
        lock.acquire() 
        balance.value = balance.value + 1
        lock.release() 
    
def perform_transactions(): 
  
    # initial balance (in shared memory) 
    balance = multiprocessing.Value('i', 100) 
  
    # creating a lock object 
    lock = multiprocessing.Lock() 
  
    # creating new processes 
    p1 = multiprocessing.Process(target=withdraw, args=(balance,lock)) 
    p2 = multiprocessing.Process(target=deposit, args=(balance,lock)) 
  
    # starting processes 
    p1.start() 
    p2.start() 
  
    # wait until processes are finished 
    p1.join() 
    p2.join() 
  
    # print final balance 
    print("Final balance = {}".format(balance.value)) 

   
for _ in range(10): 
   # perform same transaction process 10 times 
   perform_transactions() 
```

```
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
Final balance = 100
```





