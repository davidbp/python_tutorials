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
    #x = doc_cleaner(x)
    #print(len(manager_vocabulary), flush=True)
    words = doc_analyzer(sentence)
    for word in words:
        manager_vocabulary[word] += 1 

def build_sentences(n_examples):
    letters = string.ascii_lowercase + ' ' + '.'
    x = ''.join(random.choice(letters) for i in range(n_examples))
    sentences = x.split('.')
    return sentences


def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    chunksize = 100

    # Uncomment for randomly generated data
    #n_examples = 1000_000
    #sentences = build_sentences(n_examples)

    sentences, _, _, _ = load_data()
    print(f'num docs = {len(sentences)}')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()

    t0 = time.time()
    pool = Pool(processes=10)
    manager = MyManager()
    manager.start()
    manager_vocabulary = manager.defaultdict(int)

    pool.starmap(update_vocabulary, zip(sentences, repeat(manager_vocabulary), repeat(doc_analyzer)), chunksize=chunksize)
    
    print(f'time taken {t0 -time.time()} seconds')

    print('len(manager_vocabulary.items())', len(manager_vocabulary.items()))
