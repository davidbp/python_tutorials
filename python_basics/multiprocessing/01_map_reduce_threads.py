import string
import time
from collections import defaultdict
from functools import partial
from multiprocessing.dummy import Pool as ThreadPool

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



# Basic tokenizer: lowercases, strips punctuation, and splits on whitespace
def simple_tokenizer(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()

def aggregate_dicts(dicts):
    if len(dicts) == 1:
        return dicts[0]

    result = dicts[0]
    for d in dicts[1:]:
        for k, v in d.items():
            result[k] += v
    return result

def build_vocabulary(sentence):
    vocabulary = defaultdict(int)
    words = simple_tokenizer(sentence)
    for word in words:
        vocabulary[word] += 1
    return vocabulary

if __name__ == '__main__':
    n_jobs = 10
    factor_multiplier = 20  # Ensures 500k million documents

    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}\n')

    with timer('overall', indentation=''):
        with timer('build vocabularies', indentation=''):
            with ThreadPool(n_jobs) as pool:
                partial_vocabularies = pool.map(build_vocabulary, sentences)

        with timer('aggregate vocabularies', indentation=''):
            vocabulary = aggregate_dicts(partial_vocabularies)

    print('\nlen(partial_vocabularies)--->', len(partial_vocabularies))
    print('len(vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))

