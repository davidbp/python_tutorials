

import random
import multiprocessing
from multiprocessing import Pool
import time

def monte_carlo_pi_part(n):
    
    count = 0
    for i in range(n):
        x=random.random()
        y=random.random()
        
        if x*x + y*y <= 1:
            count=count+1
        
    return count

def main():

    n_threads = multiprocessing.cpu_count()
    print('You have {0:1d} CPUs'.format(n_threads))

    # Nummber of points to use for the Pi estimation
    n = 100_000_000
    t0 = time.time()

    part_count=[int(n/n_threads) for i in range(n_threads)]

    #Create the worker pool
    # http://docs.python.org/library/multiprocessing.html#module-multiprocessing.pool
    pool = Pool(processes=n_threads)   

    # parallel map
    count=pool.map(monte_carlo_pi_part, part_count)

    print("Esitmated value of Pi:: ", sum(count)/(n*1.0)*4 )
    print(f'Runtime {round(time.time()-t0,2)} sec')

if __name__=='__main__':
    main()
    
