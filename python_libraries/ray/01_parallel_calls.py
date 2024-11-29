from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ray
import time
from time import sleep

ray.init(num_cpus=10, ignore_reinit_error=True)
print('\nSuccessfully imported ray!')


def regular_function():
    sleep(2)
    return 1

@ray.remote
def remote_function():
    sleep(2)
    return 1

def sum_serial(n):
    result = 0
    for _ in range(n):
        result += regular_function()
    return result


def sum_remote(n):
    results = []
    for _ in range(n):
        results.append(remote_function.remote())
    return sum(ray.get(results))


n = 10

t0 = time.time()
print(f"\nsum_serial(n)={sum_serial(n)}")
total_time = time.time() - t0
print(f"time sum_serial={total_time}")


t0 = time.time()
print(f"\nsum_remote(n)={sum_remote(n)}")
total_time = time.time() - t0
print(f"time sum_remote={total_time}")
