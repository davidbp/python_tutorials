
import numpy as np
import time
import cy_distances


M = 786
n_cluster = 256
n_examples_per_test = [100, 256, 512, 1000, 10_000, 100_000, 500_000, 1_000_000]

for n_examples in n_examples_per_test:

	dtable = np.array(np.random.random((M, n_cluster)), 'float32')
	pq_codes_batch = np.array([np.random.randint([M]*M)])
	pq_codes_B = np.vstack([pq_codes_batch for i in range(n_examples)])

	print(f'Examples = {len(pq_codes_B)}, features={M}')
	t0 = time.time()
	cy_distances.dist_pqcodes_to_codebooks(M, dtable, pq_codes_B)
	print(f'\ttime sequential: {time.time()-t0}')
	t0 = time.time()
	cy_distances.dist_pqcodes_to_codebooks_par_n_m(M, dtable, pq_codes_B)
	print(f'\ttime parallel n_m: {time.time() - t0}')
	
	# Uncomment to see this is much worse
	#t0 = time.time()
	#cy_distances.dist_pqcodes_to_codebooks_par_m_n(M, dtable, pq_codes_B)
	#print(f'\ttime parallel m_n: {time.time() - t0}')

