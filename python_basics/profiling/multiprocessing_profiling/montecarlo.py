

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


    # Nummber of points to use for the Pi estimation
    n = 50_000_000
    t0 = time.time()

    # parallel map
    count=monte_carlo_pi_part(n)

    print("Esitmated value of Pi:: ", count/(n*1.0)*4 )
    print(f'Runtime {round(time.time()-t0,2)} sec')

if __name__=='__main__':
    main()
    
