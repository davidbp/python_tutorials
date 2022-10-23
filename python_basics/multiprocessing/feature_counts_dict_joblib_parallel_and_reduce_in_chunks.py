import string
import random
import time
from collections import Counter
from functools import partial, reduce

from collections import defaultdict
from itertools import repeat

import sklearn
from sklearn import feature_extraction, datasets
from joblib import Parallel, delayed

from utils import timer, load_data

def aggregate_dicts(dicts):

    if len(dicts) == 1:
        return dicts
    
    else:
        result = dicts[0]

        for d in dicts[1:]:
            for k,v in d.items():
                result[k] +=v
        
        return result

def build_vocabulary(sentences, doc_analyzer):
    vocabulary = defaultdict(int)
    for sentence in sentences:
        words = doc_analyzer(sentence)
        for word in words:
            vocabulary[word] += 1 

    return vocabulary

def get_batches(s, n, truncate=False):
    assert n > 0
    while len(s) >= n:
        yield s[:n]
        s = s[n:]
    if len(s) and not truncate:
        yield s

if __name__ == '__main__':

    n_jobs = 10
    chunk_size = 100_000
    factor_multiplier = 100 # This factor ensures 1 million documents in the dataset

    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier

    print(f'num docs = {len(sentences)}\n')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()

    with timer('overall', indentation=''):
        with timer('build vocabularies', indentation=''):
            p_build_vocabulary = partial(build_vocabulary,  doc_analyzer=doc_analyzer)
            partial_vocabularies = Parallel(n_jobs=n_jobs)(delayed(p_build_vocabulary)(s) for s in get_batches(sentences, chunk_size))

        with timer('aggregate vocabularies', indentation=''):
            vocabulary = aggregate_dicts(partial_vocabularies)

    print('\nlen(partial_vocabularies)--->', len(partial_vocabularies))        
    print('len(vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))
