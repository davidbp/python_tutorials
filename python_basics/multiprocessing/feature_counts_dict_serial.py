import string
import random

from collections import defaultdict
from itertools import repeat

import sklearn
from sklearn import feature_extraction, datasets

from utils import timer, load_data

def update_vocabulary(sentence, vocabulary, doc_analyzer):
    words = doc_analyzer(sentence)
    for word in words:
        vocabulary[word] +=1 

if __name__ == '__main__':

    factor_multiplier = 100 # This factor ensures 1 million documents in the dataset
    sentences, _, _, _ = load_data()
    sentences = sentences * factor_multiplier
    print(f'num docs = {len(sentences)}\n')

    count_vectorizer = feature_extraction.text.CountVectorizer()
    doc_analyzer = count_vectorizer.build_analyzer()
    vocabulary = defaultdict(int)
    
    with timer('overall', indentation=''):
        for s in sentences:
            update_vocabulary(s, vocabulary, doc_analyzer)

    print('\nlen(vocabulary.items())--->', len(vocabulary.items()))
    print("(vocabulary['from'], vocabulary['gift'])--->", (vocabulary['from'], vocabulary['gift']))

