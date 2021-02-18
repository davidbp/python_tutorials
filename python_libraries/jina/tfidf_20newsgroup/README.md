

## Basics

The logic for the jina application is in `app.py`.

The application `app.py` has two options:

- `python app.py index`: indexes the data from
  - This data is specified by the `config()` in  `os.environ['JINA_DATA_PATH']='dataset/20_newsgroup.csv'` 
- `python app.py search`: Presents a terminal interface where a user can write a query (document or sentence) and returns the `top_k` results (in the code `top_k=2`).

**Before** running `app.py` the user needs to run

- `python 01_fetch_dataset.py`: Create a `dataset` folder with the `20newsgroup` dataset.
- `python 02_build_tfidf.py`:  Create a TF-IDF encoder and stores it in `/pods/tfidf_vectorizer.pickle`.



## Insights on  `app.py`



### Custom TFIDFTextEncoder encoder

This application creates a custom encoder, that is named`TFIDFTextEncoder`. 

This encoder can be found in  `pods/tfidf_vectorizer_jina.py` and it contains the following code:

```python
from jina.executors.encoders import BaseEncoder
from jina.executors.decorators import batching, as_ndarray
import numpy as np
import pickle

class TFIDFTextEncoder(BaseEncoder):
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
```

This code creates a class that inherits from `BaseEncoder` and it contains the methods:

- **`post_init`**: loads the model from a `path_vectorizer`.
- **`encode`**: Gets as input a batch of data and transforms it.



### Searching items 

We can call `python app.py search` to search items.

Note that running `search` will call `search()` which is is the following function

```python
def search():
    f = Flow.load_config('flows/query.yml')
    with f:
        while True:
            text = input("Introduce a sentece as query: ")
            if not text:
                break
            def ppr(x):
                print_resp(x, text)
            f.search_lines(lines=[text, ], on_done=ppr, top_k=2, line_format=None)
```

This function calls `f.search_lines` which is refers to  `CRUDFlowMixin.search_lines` the help function of `f.search_lines` states that the function:   ` Use a list of lines as the index source for indexing on the current Flow`.



