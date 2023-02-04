
from multiprocessing import Process, Manager

import sklearn

def f(vocabulary_, sentences):
    pass

def load_data():

    X = sklearn.datasets.fetch_20newsgroups()

    X_train = sklearn.datasets.fetch_20newsgroups(subset="train").data
    y_train = sklearn.datasets.fetch_20newsgroups(subset="train").target
    X_test  = sklearn.datasets.fetch_20newsgroups(subset="test").data
    y_test  = sklearn.datasets.fetch_20newsgroups(subset="test").target

    return X_train, y_train, X_test, y_test


if __name__ == '__main__':

    X_train, y_train, X_test, y_test = load_data()

    manager = Manager()
    vocabulary_ = manager.dict()

    p1 = Process(target=f, args=(vocabulary_,sentences[1:1000]))
    p2 = Process(target=f, args=(vocabulary_,sentences[1000:end]))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print(vocabulary_)

