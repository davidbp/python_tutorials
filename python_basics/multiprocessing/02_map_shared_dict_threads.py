import string
import time
from collections import defaultdict
from threading import Lock
from multiprocessing.dummy import Pool as ThreadPool

import sklearn
from sklearn import datasets


class timer:
    def __init__(self, name='', indentation=''):
        self.start = time.time()
        self.name = name
        self.indentation = indentation

    def __enter__(self):
        pass

    def __exit__(self, *args):
        print(self.indentation + f'time {self.name}  {round(time.time() - self.start, 4)} sec')


def load_data():
    X_train = datasets.fetch_20newsgroups(subset="train").data
    y_train = datasets.fetch_20newsgroups(subset="train").target
    X_test = datasets.fetch_20newsgroups(subset="test").data
    y_test = datasets.fetch_20newsgroups(subset="test").target
    return X_train, y_train, X_test, y_test


# Basic tokenizer: lowercases, strips punctuation, and splits on whitespace
def simple_tokenizer(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()


# Shared resources for all threads
shared_vocabulary = defaultdict(int)
vocab_lock = Lock()


def update_shared_vocabulary(sentence):
    words = simple_tokenizer(sentence)
    with vocab_lock:
        for word in words:
            shared_vocabulary[word] += 1


if __name__ == '__main__':
    n_jobs = 10
    factor_multiplier = 20  # Ensures ~200k documents

    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}\n')

    with timer('overall', indentation=''):
        with timer('build vocabularies (shared dict)', indentation=''):
            with ThreadPool(n_jobs) as pool:
                pool.map(update_shared_vocabulary, sentences)

    print('\nlen(vocabulary.items())--->', len(shared_vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (shared_vocabulary['from'], shared_vocabulary['gift']))

