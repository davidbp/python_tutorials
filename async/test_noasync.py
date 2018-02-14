import time
import random

def example_coroutine(i):
    time_io_wait = random.randint(1,3)
    time.sleep(time_io_wait)   # This simulates waiting some function 
                                  # to recieve info from the internet for example
    print("example {} execyted after {} seconds".format(i,time_io_wait))

def main():
    tasks = []
    for i in range(20):
        tasks.append(example_coroutine(i))

t0=time.time()
main()
print("\nTotal time needed was {}\n".format(time.time() -t0 ) )