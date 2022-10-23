# Collection of parallelizable examples


## Feature counts

Example building a dict that contains word counts.

Serial version (bottlenecked by the completly serial operation)
```
python feature_counts_dict_serial.py 
```

```
num docs = 1131400

time overall  117.3199 sec

len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
```


Parallel version working one element at a time (bottlenecked by the reduce step)

```
python feature_counts_dict_joblib_parallel_and_reduce.py
```

```
num docs = 1131400

time build vocabularies  42.0592 sec
time aggregate vocabularies  35.4708 sec
time overall  77.5302 sec

len(partial_vocabularies)---> 1131400
len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
```


Parallel version working in minibatches (not bottlenecked in the parallel part, irrelevant bottlenecked in the reduce step)
```
python feature_counts_dict_joblib_parallel_and_reduce_in_chunks.py
```

```
num docs = 1131400

time build vocabularies  26.7191 sec
time aggregate vocabularies  0.236 sec
time overall  26.9552 sec

len(partial_vocabularies)---> 12
len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
```
