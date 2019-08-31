import time

from python_code import fib
from cython_code import fib_cy


start = time.time()

for i in range(35):
    fib.fib(i)

end = time.time()
res = end-start
print("total time fib.fib method is {} seconds".format(res))



start = time.time()

for i in range(35):
     fib_cy.fib(i)

end = time.time()
res = end-start
print("total time fib_cy.fib method is {} seconds".format(res))
