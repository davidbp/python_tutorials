import string
import random

from multiprocessing import Pool
from collections import defaultdict
from itertools import repeat

import sklearn
from sklearn import feature_extraction, datasets
import time
from functools import partial, reduce
from collections import Counter


def aggregate_dicts(dicts, operation=sum):
    all_keys = set().union(*[el.keys() for el in dicts])
    return {k: sum([dic.get(k, 0) for dic in dicts]) for k in all_keys}

def build_vocabulary(sentence, doc_analyzer):
    vocabulary = defaultdict(int)
    words = doc_analyzer(sentence)

    for word in words:
        vocabulary[word] += 1 
    return vocabulary

def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    n_jobs = 10
    chunksize = 1000

    factor_multiplier = 100 # This factor ensures 1 million documents in the dataset
    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}')


    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()

    t0 = time.time()
    pool = Pool(processes=n_jobs)

    p_build_vocabulary = partial(build_vocabulary,  doc_analyzer=doc_analyzer)
    partial_vocabularies = pool.map(p_build_vocabulary, sentences) 
    print('len(partial_vocabularies)--->', len(partial_vocabularies))
    vocabulary = aggregate_dicts(partial_vocabularies)
    # An alternative way could be to use counter objects
    #vocabulary = reduce(lambda a,b: Counter(a)+Counter(b), partial_vocabularies)

    print(f'time taken {time.time()-t0} seconds')
    print('len(manager_vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))
