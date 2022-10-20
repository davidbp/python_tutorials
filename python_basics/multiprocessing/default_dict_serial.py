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

def update_vocabulary(sentence, vocabulary, doc_analyzer):
    words = doc_analyzer(sentence)
    for word in words:
        vocabulary[word] = len(vocabulary)


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
    vocabulary = defaultdict(int)

    t0 = time.time()
    
    for s in sentences:
        update_vocabulary(s, vocabulary, doc_analyzer)

    print(f'time taken {time.time() - t0} seconds')
    print('len(vocabulary.items())', len(vocabulary.items()))
