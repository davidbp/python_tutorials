import time
import random

def example_coroutine(i):
    time_io_wait = 3
    time.sleep(time_io_wait)   
    
def main():
    tasks = []
    t0 = time.time()
    for i in range(5):
        print(f'time after iter {i} is {time.time()-t0}')
        tasks.append(example_coroutine(i))

t0=time.time()
main()
print("\nTotal time needed was {}\n".format(time.time() -t0 ) )