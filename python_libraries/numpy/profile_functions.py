import numpy as np
import functions
from functions import utils

import memory_profiler
import timeit
from line_profiler import LineProfiler


n = 10000
ids = np.random.permutation(n)
scores = np.random.rand(n)
r = [(i,s) for i,s in zip(ids,scores)]

def test_sort_by_score_1():
    utils.sort_by_score_1(r)

def test_sort_by_score_2():
    utils.sort_by_score_2(r)

if __name__ == '__main__':
   
    #print('tiemit:', timeit.timeit(lambda: "-".join(map(str, range(100))), number=10000))
    print('time test_sort_by_score_1:', timeit.timeit('test_sort_by_score_1()', setup="from __main__ import test_sort_by_score_1", number=100))
    print('time test_sort_by_score_2:', timeit.timeit('test_sort_by_score_2()', setup="from __main__ import test_sort_by_score_2", number=100))
    #timeit.timeit(utils.sort_by_score_1(r))

    #utils.sort_by_score_1(r)
    #utils.sort_by_score_2(r)
    #lp = LineProfiler()
    #lp_wrapper = lp(utils.main)
    #lp_wrapper()
    #lp.print_stats()