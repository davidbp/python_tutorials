# Collection of parallelizable examples


## Feature counts

Example building a dict that contains word counts.

Serial version (bottlenecked by the completly serial operation)
```
python feature_counts_dict_serial.py 
```

```
num docs = 1131400
len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
time taken 133.69434714317322 seconds
```


Parallel version working one element at a time (bottlenecked by the reduce step)

```
python feature_counts_dict_joblib_parallel_and_reduce.py
```

```
num docs = 1131400
len(partial_vocabularies)---> 1131400
len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
time taken 76.5679018497467 seconds
```


Parallel version working in minibatches (not bottlenecked in the parallel part, a bit bottlenecked in the reduce step)
```
python feature_counts_dict_joblib_parallel_and_reduce_in_chunks.py
```

```
num docs = 1131400
len(partial_vocabularies)---> 12
len(vocabulary.items())---> 130107
(vocabulary['from'], vocabulary['gift'])---> (2267000, 6600)
time taken 26.82607889175415 seconds
```
