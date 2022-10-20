import string
import random

from multiprocessing import Pool
from multiprocessing.managers import BaseManager, DictProxy
from collections import defaultdict
from itertools import repeat

import sklearn
from sklearn import feature_extraction, datasets
import time

class MyManager(BaseManager):
    pass

MyManager.register('defaultdict', defaultdict, DictProxy)

def update_vocabulary(sentence, manager_vocabulary, doc_analyzer):
    words = doc_analyzer(sentence)
    for word in words:
        manager_vocabulary[word] += 1 

def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    n_jobs = 10
    chunksize = 100

    factor_multiplier = 100 # This factor ensures 1 million documents in the dataset
    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()

    t0 = time.time()
    pool = Pool(processes=n_jobs)
    manager = MyManager()
    manager.start()
    manager_vocabulary = manager.defaultdict(int)

    pool.starmap(update_vocabulary, zip(sentences, repeat(manager_vocabulary), repeat(doc_analyzer)), chunksize=chunksize)
    vocabulary = manager_vocabulary
    
    print('len(vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))
    print(f'time taken {time.time()-t0} seconds')

