import timeit

cy_time = timeit.timeit("cy_func.sum(10)",   setup="import cy_func", number=1000)
cy2_time = timeit.timeit("cy_func2.sum(10)", setup="import cy_func2", number=1000)
py_time = timeit.timeit("py_func.sum(10)",   setup="from python_code import py_func", number=1000)

print("\nResults for 10")
print("\tcython non typed time: ", cy_time)
print("\tcython typed time:     ", cy2_time)
print("\tpython time:           ", py_time)
print("\tCython (non typed) is {} times faster than python". format(py_time/cy_time))
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy2_time))



cy_time = timeit.timeit("cy_func.sum(1_000)",   setup="import cy_func", number=1000)
cy2_time = timeit.timeit("cy_func2.sum(1_000)", setup="import cy_func2", number=1000)
py_time = timeit.timeit("py_func.sum(1_000)",   setup="from python_code import py_func", number=1000)

print("\nResults for 1_000")
print("\tcython non typed time: ", cy_time)
print("\tcython typed time:     ", cy2_time)
print("\tpython time:           ", py_time)
print("\tCython (non typed) is {} times faster than python". format(py_time/cy_time))
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy2_time))




cy_time = timeit.timeit("cy_func.sum(10_000)",   setup="import cy_func", number=1000)
cy2_time = timeit.timeit("cy_func2.sum(10_000)", setup="import cy_func2", number=1000)
py_time = timeit.timeit("py_func.sum(10_000)",   setup="from python_code import py_func", number=1000)

print("\nResults for 10_000")
print("\tcython non typed time: ", cy_time)
print("\tcython typed time:     ", cy2_time)
print("\tpython time:           ", py_time)
print("\tCython (non typed) is {} times faster than python". format(py_time/cy_time))
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy2_time))