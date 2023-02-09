import string
import random

from multiprocessing import Pool
from multiprocessing.managers import BaseManager, DictProxy
from collections import defaultdict

import sklearn
from sklearn import feature_extraction, datasets

class MyManager(BaseManager):
    pass

MyManager.register('defaultdict', defaultdict, DictProxy)

def update_vocabulary(sentence, manager_vocabulary, doc_cleaner, doc_tokenizer):
    #x = doc_cleaner(x)
    words = doc_tokenizer(sentence)
    for word in words:
        manager_vocabulary[word] = len(manager_vocabulary)


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

    # Uncomment for randomly generated data
    #n_examples = 1000_000
    #sentences = build_sentences(n_examples)

    sentences, _, _, _ = load_data()
    sentences = sentences[0:1000]
    print(f'num docs = {len(sentences)}')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_cleaner = count_vectorizer.build_preprocessor()
    doc_tokenizer = count_vectorizer.build_tokenizer()

    pool = Pool(processes=10)
    manager = MyManager()
    manager.start()
    manager_vocabulary = manager.defaultdict(int)

    for sentence in sentences:
        pool.apply_async(update_vocabulary, (sentence, manager_vocabulary, doc_cleaner, doc_tokenizer))

    pool.close()
    pool.join()

    print(manager_vocabulary.items())
