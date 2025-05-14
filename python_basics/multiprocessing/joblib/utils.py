import time

import sklearn
from sklearn import feature_extraction, datasets

class timer():

    def __init__(self, name = '', indentation=''):
        self.start = time.time()
        self.name = name
        self.indentation = indentation

    def __enter__(self):
        pass

    def __exit__(self, *args):
        print(self.indentation + f'time {self.name}  {round(time.time() - self.start, 4)} sec')


def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test

