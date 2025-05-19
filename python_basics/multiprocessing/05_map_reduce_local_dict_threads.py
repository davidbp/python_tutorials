import string
import time
from collections import defaultdict
from threading import Lock
from multiprocessing.dummy import Pool as ThreadPool

import sklearn
from sklearn import datasets
from collections import Counter


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


def build_local_vocabulary(sentences_chunk):
    local_vocab = Counter()
    for sentence in sentences_chunk:
        words = simple_tokenizer(sentence)
        local_vocab.update(words)
    return local_vocab

if __name__ == '__main__':
    from math import ceil

    n_jobs = 10
    factor_multiplier = 20

    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}\n')

    chunk_size = ceil(len(sentences) / n_jobs)
    chunks = [sentences[i:i + chunk_size] for i in range(0, len(sentences), chunk_size)]

    with timer('overall'):
        with timer('build vocabularies (local merge)'):
            with ThreadPool(n_jobs) as pool:
                local_vocabularies = pool.map(build_local_vocabulary, chunks)

            # Merge all local vocabularies into one
            merged_vocab = Counter()
            for vocab in local_vocabularies:
                merged_vocab.update(vocab)

    print('\nlen(vocabulary.items())--->', len(merged_vocab.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (merged_vocab['from'], merged_vocab['gift']))

