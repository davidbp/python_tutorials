
import numpy as np
import h5py
import cProfile

# Ordinary numpy array
arr = np.arange(5_000_000)

# Memory map
nmmarr = np.memmap(shape=arr.shape, filename="./benchmark.nmm", mode='w+')
nmmarr[:] = arr[:]

# hdf5 file
f = h5py.File("./benchmark.hdf5", "w", driver='core')
d = f.create_dataset("mydataset", arr.shape, dtype=arr.dtype)

d[:] = arr[:]
f.close()
f = h5py.File("./benchmark.hdf5", "r", driver='core')

hdarr = f.get('mydataset')


# test function
def run(x, bs=10000):
    print(f'\n\ntype(x)={type(x)}\n\n')
    total = 0
    for i in range(len(x)//bs):
        #print(i)
        total+= sum(x[(i*bs):((i+1)*bs)])
    print(f'result={total}')


cProfile.run('run(nmmarr)')  # painfully slow

cProfile.run('run(arr)')  # clearly the fastest way

# much faster than the numpy.memmap alternative
cProfile.run('run(hdarr)')
