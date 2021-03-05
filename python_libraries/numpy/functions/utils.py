from memory_profiler import profile
import numpy as np

#@profile
def sort_by_score_1(r):
    r = np.array(r,dtype=[('ids',np.int),('scores',np.float64)])
    return np.sort(r, order='scores')[::-1]

#@profile
def sort_by_score_2(r: [(any,any)]):
    scores = np.array([r_k[1] for r_k in r])
    sorted_ids = scores.argsort()[::-1]
    r_sorted_np = np.array([r[i] for i in sorted_ids],
                           dtype=[('ids',np.int),('scores',np.float64)])
    return r_sorted_np
    
def main():
    n = 10000
    ids = np.random.permutation(n)
    scores = np.random.rand(n)
    r = [(i,s) for i,s in zip(ids,scores)]
    sort_by_score_1(r)

if __name__=='__main__':
    main()
   