

cpdef fib(int n):
    if n==0 or n==1 :
        return n
    result = fib(n-1) + fib(n-2)
    return result
