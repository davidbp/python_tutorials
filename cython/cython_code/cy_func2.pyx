
"""

We can specify the type of the returned objects in the input:

	cpdef return_type function(type a1, type a2 ,...)

For example

	cpdef int sum(int n)


"""

cpdef int sum(int n):
    cdef:
        int s = 0
        int i

    for i in range(n):
        s +=i

    return s

