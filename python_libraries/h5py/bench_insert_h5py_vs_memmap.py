
import numpy as np
import h5py
import cProfile
import os
import shutil
import time

def insert_data(x, arr, bs=10_000):
    print('\n\nINSERT DATA')
    print(f'\n\ntype(x)={type(x)}\n\n')
    total = 0
    for i in range(len(x)//bs):
        beg_ind = int((i*bs))
        end_ind = int((i+1)*bs)
        x[beg_ind:end_ind] = arr[beg_ind:end_ind]


def insert_data_online(x, n_examples, n_features, batch_size=10_000):
    print('\n\nINSERT DATA ONLINE')
    print(f'\n\ntype(x)={type(x)}\n\n')
    batch_generator = create_data_online(n_examples, n_features, batch_size)

    total = 0
    for Xbatch, start_ind, end_ind in batch_generator:
        print(Xbatch.shape, start_ind, end_ind)
        x[start_ind:end_ind] = Xbatch
    

def load_data(x, bs=1_000):
    print('\n\nLOAD DATA')
    print(f'type(x)={type(x)}\n\n')
    total = 0
    for i in range(len(x)//bs):
        beg_ind = int((i*bs))
        end_ind = int((i+1)*bs)
        total += np.sum(x[beg_ind:end_ind])
    print(f'result={total}')


def clean_workspace():
    if os.path.exists('benchmark.hdf5'):
        os.remove('benchmark.hdf5')

    if os.path.exists('benchmark.nmm'):
        os.remove('benchmark.nmm')


def create_data_online(n_examples, n_features, batch_size):
    np.random.seed(123)
    num = 0
    while True:
        X_batch = np.random.rand(batch_size, n_features).astype(np.float32)

        if num + batch_size >= n_examples:
            break
        else:
            yield X_batch, num, num+batch_size
            num += batch_size
    
    if num < n_examples:
        X_batch = np.random.rand(23, n_features).astype(np.float32)
        yield X_batch, num, n_examples
        num += batch_size


clean_workspace()
n_features = 512
n_examples = 1_000_000
arr = np.empty((n_examples, n_features))+1

############################ insert_data ############################
np_memmap = np.memmap(shape=arr.shape, filename="./benchmark.nmm", mode='w+')
cProfile.run('insert_data(np_memmap, arr)') 
#insert_data(np_memmap, arr)

f = h5py.File("./benchmark.hdf5", "w", driver='core')
hdf5_arr = f.create_dataset("mydataset", arr.shape, dtype=arr.dtype)
cProfile.run('insert_data(hdf5_arr, arr)') 
#insert_data(hdf5_arr, arr)
f.close()


############################ insert_data_online ############################

clean_workspace()
n_features_online = 512
n_examples_online = 2_000_000

np_memmap = np.memmap(shape=arr.shape, filename="./benchmark.nmm", mode='w+')
t0 = time.time()
insert_data_online(np_memmap, n_examples_online, n_features_online)
t1 = time.time() - t0
print(f'\n\n time insert_data_online(np_memmap) = {t1}\n\n')
#cProfile.run('insert_data_online(np_memmap, n_examples_online, n_features_online)') 

print('start hdf5')
f = h5py.File("./benchmark.hdf5", "w", driver='core')
hdf5_arr = f.create_dataset("mydataset", n_examples_online, dtype=np.float32)
t0 = time.time()
insert_data_online(hdf5_arr,  n_examples_online, n_features_online)
t1 = time.time() - t0
print(f'\n\n time insert_data_online(hdf5_arr) = {t1}\n\n')
#cProfile.run('insert_data_online(hdf5_arr,  n_examples_online, n_features_online)') 

f.close()


############################ load_data ############################
"""
np_memmap = np.memmap(shape=arr.shape, filename="./benchmark.nmm", mode='r')
cProfile.run('load_data(np_memmap)') 
#load_data(np_memmap)

f2 = h5py.File("./benchmark.hdf5", "r", driver='core')
hdf5_arr2 = f2.get('mydataset') #f2['mydataset']
cProfile.run('load_data(hdf5_arr2)') 
"""