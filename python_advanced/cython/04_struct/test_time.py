import timeit

N = 1000
cy_time = timeit.timeit(f"cy_func.verify_rectangles({N})",   setup="import cy_func", number=100)
py_time = timeit.timeit(f"py_func.verify_rectangles({N})",   setup="from python_code import py_func", number=100)

print(f"\nResults for N={N} rectangles")
print("\tcython non typed time: ", cy_time)
print("\tpython time:           ", py_time)
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy_time))


N = 10000
cy_time = timeit.timeit(f"cy_func.verify_rectangles({N})",   setup="import cy_func", number=100)
py_time = timeit.timeit(f"py_func.verify_rectangles({N})",   setup="from python_code import py_func", number=100)

print(f"\nResults for N={N} rectangles")
print("\tcython non typed time: ", cy_time)
print("\tpython time:           ", py_time)
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy_time))

N = 100000
cy_time = timeit.timeit(f"cy_func.verify_rectangles({N})",   setup="import cy_func", number=100)
py_time = timeit.timeit(f"py_func.verify_rectangles({N})",   setup="from python_code import py_func", number=100)


print(f"\nResults for N={N} rectangles")
print("\tcython non typed time: ", cy_time)
print("\tpython time:           ", py_time)
print("\tCython (typed) is {} times faster than python    ". format(py_time/cy_time))


