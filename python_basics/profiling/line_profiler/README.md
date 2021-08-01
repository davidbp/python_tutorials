### Benchmark

The script  **`bench_tests.py`**  contains three functions with `@profile`  that$

```python
kernprof -l bench_tests.py
```

This will create a file `bench_tests.py.lprof`. 

The following command 


```python
python -m line_profiler bench_tests.py.lprof
```

will show the otuptus of the benchmark.


```
File: bench_tests.py
Function: main_func at line 42

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    42                                           @profile
    43                                           def main_func():
    44         1       6366.0   6366.0     35.9      result = atribute_from_clas$
    45         1         53.0     53.0      0.3      print(result)
    46
    47         1       5552.0   5552.0     31.3      result = property_from_clas$
    48         1          9.0      9.0      0.1      print(result)
    49
    50         1       5741.0   5741.0     32.4      result = method_from_class()
    51         1          8.0      8.0      0.0      print(result)
```

