import timeit

cy_time = timeit.timeit("cy_func.count_greater(10)",   setup="import cy_func", number=1000)
py_time = timeit.timeit("py_func.count_greater(10)",   setup="from python_code import py_func", number=1000)

print("\nResults for 10")
print("\tcython non typed time: ", cy_time)
print("\tpython time:           ", py_time)
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy_time))

