import pandas as pd
import numpy as np
import time
from multiprocessing import Pool
from time import sleep


def sum_feat(x):
	"""
	Siulates some fast computation
	"""
	return np.sum(x.features)

def sum_feat_with_io(x, io_simulation_time=0.1):
	"""
	Simulates some work that needs some time 
	(for example for downloading data or long compute)
	"""
	sleep(io_simulation_time)
	return np.sum(x.features)


if __name__ == '__main__':

	n_rows = 1000
	n_features = 100

	X = np.random.random((n_rows, n_features))
	ids = [str(i) for i in range(len(X))]
	df = pd.DataFrame({'features':[x for x in X] , 'id': ids})


	### Soution with Pool ###
	t0 = time.time()
	n_proc = 10
	pool = Pool(n_proc)
	result_1 = pool.map(sum_feat_with_io, (x[1] for x in df.iterrows()))
	pool.close()
	pool.join()
	print(f'time Pool {time.time()-t0} sec')


	### Solution with apply ####
	t0 = time.time()
	result_2 = df.apply(sum_feat_with_io, axis=1)
	print(f'time apply {time.time()-t0} sec')


	# check result is the same
	print('all(result_2 == result_1) ->',all(result_2 == result_1))
