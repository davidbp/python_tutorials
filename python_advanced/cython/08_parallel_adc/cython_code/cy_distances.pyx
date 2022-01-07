
from libcpp.vector cimport vector
from cython.parallel import prange, parallel

import numpy as np
cimport numpy as np
cimport cython

from cpython.array cimport array, clone


@cython.boundscheck(False)
@cython.wraparound(False)
cdef inline float dist_pqcode_to_codebook(long M, float[:,:] dtable,long[:] pq_code):
    cdef float dist = 0
    cdef int m
    
    for m in range(M):
        dist += dtable[m, pq_code[m]]

    return dist


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dist_pqcodes_to_codebooks(const long M, float[:,:] dtable, long[:,:] pq_codes):
    cdef:
        int m, loops
        int N = pq_codes.shape[0] 
        #float[:] dists = np.empty(N, dtype=np.float32)
        vector[float] dists
    
    for n in range(N):
        dists.push_back(dist_pqcode_to_codebook(M, dtable, pq_codes[n,:]))

    return np.asarray(dists)


@cython.boundscheck(False)
@cython.wraparound(False)
cdef dist_pqcodes_to_codebooks_parfor_n_m(const long D, 
                                      const long N,
                                      const long M, 
                                      const float[:,:] dtable, 
                                      const long[:,:] pq_codes,
                                      float[:] dists):
    cdef int m, n
    
    with nogil:
        for n in prange(N, schedule='dynamic'):
            for m in range(M):
                dists[n] += dtable[m, pq_codes[n, m]]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dist_pqcodes_to_codebooks_par_n_m(const long M, 
                                    const float[:,:] dtable,
                                    const long[:,:] pq_codes):
    cdef:
        int m, loops
        int N = pq_codes.shape[0]
        int D = pq_codes.shape[1]
        float[:] dists = np.zeros(N, dtype=np.float32)
    
    dist_pqcodes_to_codebooks_parfor_n_m(D, N, M, dtable, pq_codes, dists)
    
    return np.array(dists) 


@cython.boundscheck(False)
@cython.wraparound(False)
cdef dist_pqcodes_to_codebooks_parfor_m_n(const long D, 
                                      const long N,
                                      const long M, 
                                      const float[:,:] dtable, 
                                      const long[:,:] pq_codes,
                                      float[:] dists):
    cdef int m, n
    
    for m in prange(M, schedule='dynamic', nogil=True):
        for n in range(N):
            dists[n] += dtable[m, pq_codes[n, m]]


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef dist_pqcodes_to_codebooks_par_m_n(const long M, 
                                    const float[:,:] dtable,
                                    const long[:,:] pq_codes):
    cdef:
        int m, loops
        int N = pq_codes.shape[0]
        int D = pq_codes.shape[1]
        float[:] dists = np.zeros(N, dtype=np.float32)
    
    dist_pqcodes_to_codebooks_parfor_m_n(D, N, M, dtable, pq_codes, dists)
    
    return np.array(dists) 

