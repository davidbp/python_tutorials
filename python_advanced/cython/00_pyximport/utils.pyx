from cython cimport cdivision, boundscheck, wraparound

@boundscheck(False)
@wraparound(False)
cpdef geq_than_k(long[:] x,long k):
    
    cdef int n_bigger_than_k = 0
    cdef int n_x = len(x)
    
    for i in range(n_x):
        n_bigger_than_k += x[i] >= k
    
    return n_bigger_than_k, float(n_bigger_than_k)/n_x
