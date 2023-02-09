
from random import random
from time import sleep
from multiprocessing.pool import Pool

def multi_run_wrapper(args):
   return task(*args)

def task(identifier, id):
    value = random()
    print(f'Task {identifier} executing with {id}', flush=True)
    sleep(1)
    return value
 
# protect the entry point
if __name__ == '__main__':
    n_examples = 1000
    chunksize = 100

    with Pool(10) as pool:
        pool.map(multi_run_wrapper, ((x,y) for x,y in zip(range(n_examples),range(n_examples))) , chunksize=chunksize)
