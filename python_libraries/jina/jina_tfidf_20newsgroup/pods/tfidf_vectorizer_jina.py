
# base encoder implementation

from jina.executors.encoders import BaseEncoder
from jina.executors.decorators import batching, as_ndarray
import numpy as np
import pickle

class TFIDFTextEncoder(BaseEncoder):
    """
    """
    def __init__(self,
                 path_vectorizer= "./pods/tfidf_vectorizer.pickle",
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.path_vectorizer = path_vectorizer

    def post_init(self):
        self.tfidf_vectorizer = pickle.load(open(self.path_vectorizer, "rb"))

    @batching
    @as_ndarray
    def encode(self, data: np.ndarray, *args, **kwargs) -> 'np.ndarray':
        return self.tfidf_vectorizer.transform(data).toarray()

# after indexing the data is stored in ./workspace
# vec.gz: embeddings
# doc.gz: jsons with the information similar to  Document.__dict__ 
# vecidx.bin: information from vec.gz

# try to load vec.gz: n_examples x n_features  

# 8597
#             with gzip.open(abspath, 'rb') as fp:
#                return np.frombuffer(fp.read(), dtype=self.dtype).reshape([-1, self.num_dim])

# def load_vec(path, n_features = 8597):
#     with gzip.open(path, 'rb') as fp:
#         return np.frombuffer(fp.read(), dtype=np.float64).reshape([-1, n_features])



