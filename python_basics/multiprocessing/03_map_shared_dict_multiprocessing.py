import string
import time
from collections import defaultdict
from multiprocessing import Pool, Manager, Lock

import sklearn
from sklearn import datasets


class timer:
    def __init__(self, name='', indentation=''):
        self.start = time.time()
        self.name = name
        self.indentation = indentation

    def __enter__(self):
        return self

    def __exit__(self, *args):
        print(self.indentation + f'time {self.name}  {round(time.time() - self.start, 4)} sec')


def load_data():
    X_train = datasets.fetch_20newsgroups(subset="train").data
    y_train = datasets.fetch_20newsgroups(subset="train").target
    X_test = datasets.fetch_20newsgroups(subset="test").data
    y_test = datasets.fetch_20newsgroups(subset="test").target
    return X_train, y_train, X_test, y_test


# Tokenizer: lowercase, remove punctuation, split
def simple_tokenizer(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()


# This function is called by each process
def update_shared_vocabulary_old(sentence, shared_dict, lock):
    local_counts = defaultdict(int)
    for word in simple_tokenizer(sentence):
        local_counts[word] += 1

    with lock:
        for word, count in local_counts.items():
            shared_dict[word] = shared_dict.get(word, 0) + count


def update_shared_vocabulary(sentence, shared_dict, lock):
    # Local count first — no locking needed
    local_counts = defaultdict(int)
    for word in simple_tokenizer(sentence):
        local_counts[word] += 1

    # Only lock once to update the shared dict
    with lock:
        for word, count in local_counts.items():
            shared_dict[word] = shared_dict.get(word, 0) + count

def init_process(shared_dict_, lock_):
    global shared_dict
    global lock
    shared_dict = shared_dict_
    lock = lock_


def wrapper(sentence):
    update_shared_vocabulary(sentence, shared_dict, lock)


if __name__ == '__main__':
    n_jobs = 8  # or os.cpu_count()
    factor_multiplier = 20  # ~500k documents

    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}\n')

    with timer('overall', indentation=''):
        with Manager() as manager:
            shared_dict = manager.dict()
            lock = manager.Lock()

            with timer('build vocabularies (multiprocessing)', indentation=''):
                with Pool(processes=n_jobs, initializer=init_process, initargs=(shared_dict, lock)) as pool:
                    pool.map(wrapper, sentences)

            vocabulary = dict(shared_dict)  # Convert managed dict to normal dict for inspection

    print('\nlen(vocabulary.items())--->', len(vocabulary))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary.get('from', 0), vocabulary.get('gift', 0)))

