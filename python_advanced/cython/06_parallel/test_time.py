import numpy as np
import time
import juliacy

X, Y = np.meshgrid(np.linspace(-2.0 , 2.0,10000), np.linspace(-2.0, 2.0, 10000))
julia = np.zeros_like(X, dtype=np.int32)
c = -0.9 + 0.22143j
radius2 = 4.0


t0 = time.time()
juliacy.julia_set_cython_seq(X, Y, c.real, c.imag, 100, radius2, julia)
print(f'time sequential:{time.time()-t0}')


t0 = time.time()
juliacy.julia_set_cython_par(X, Y, c.real, c.imag, 100, radius2, julia)
print(f'time parallel:{time.time() - t0}')