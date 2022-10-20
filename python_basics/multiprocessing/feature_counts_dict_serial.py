import string
import random

from collections import defaultdict
from itertools import repeat

import sklearn
from sklearn import feature_extraction, datasets
import time

def update_vocabulary(sentence, vocabulary, doc_analyzer):
    words = doc_analyzer(sentence)
    for word in words:
        vocabulary[word] +=1 

def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    chunksize = 1000

    sentences, _, _, _ = load_data()
    print(f'num docs = {len(sentences)}')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()
    vocabulary = defaultdict(int)

    t0 = time.time()
    
    for s in sentences:
        update_vocabulary(s, vocabulary, doc_analyzer)

    print(f'time taken {time.time()-t0} seconds')
    print('len(vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))

