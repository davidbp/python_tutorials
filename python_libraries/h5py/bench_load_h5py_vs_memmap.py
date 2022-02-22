

import numpy as np
import h5py
import cProfile
import os
import shutil



def load_data(x, bs=10_000):
    print('\n\nLOAD DATA')
    print(f'type(x)={type(x)}\n\n')
    total = 0
    for i in range(len(x)//bs):
        beg_ind = int((i*bs))
        end_ind = int((i+1)*bs)
        total += np.sum(x[beg_ind:end_ind])
    print(f'result={total}')


############################ load_data ############################

np_memmap = np.memmap(filename="./benchmark.nmm", mode='r')
cProfile.run('load_data(np_memmap)') 

f2 = h5py.File("./benchmark.hdf5", "r", driver='core')
hdf5_arr2 = f2['mydataset']
cProfile.run('load_data(hdf5_arr2)') 

