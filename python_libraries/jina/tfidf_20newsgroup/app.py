__version__ = '0.0.1'

import os
import sys
from jina.flow import Flow
from jina import Document


def config():
    """
    Configure environment variables.
    """
    parallel = 1 if sys.argv[1] == 'index' else 1
    shards = 1
    os.environ['JINA_PARALLEL'] = str(parallel)
    os.environ['JINA_SHARDS'] = str(shards)
    os.environ['WORKDIR'] = './workspace'
    os.makedirs(os.environ['WORKDIR'], exist_ok=True)
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(65481))
    os.environ['JINA_DATA_PATH'] = 'dataset/20_newsgroup.csv'


def index_generator():
    """
    Define data as Document to be indexed.
    """
    import csv
    data_path = os.path.join(os.path.dirname(__file__), os.environ['JINA_DATA_PATH'])

    # Get Document and ID
    with open(data_path) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader, None)  # skip the header from 20newsgroup dataset
        for i, data in enumerate(reader):
            d = Document()
            # docid
            d.tags['id'] = int(data[0])
            # doc
            d.text = data[1]
            yield d


def index():
    """
    Index data using Index Flow.
    """
    f = Flow.load_config('flows/index.yml')

    with f:
        f.index(input_fn=index_generator, batch_size=512)


def print_resp(resp, text):
    """
    Print response.
    """
    for d in resp.search.docs:
        print(f"Ranked list of related documents: {text} \n")

        # d.matches contains the closests top_k documents in order 
        # from closer to farther from the query.
        for idx, match in enumerate(d.matches):

            score = match.score.value
            if score < 0.0:
                continue
            answer = match.text.strip()
            print(f'> {idx+1:>2d}. "{answer}"\n Score: ({score:.2f})')


def search():
    """
    Search results using Query Flow.
    """
    f = Flow.load_config('flows/query.yml')

    with f:
        while True:
            text = input("Introduce a sentece as query: ")
            if not text:
                break

            def ppr(x):
                print_resp(x, text)

            f.search_lines(lines=[text, ], on_done=ppr, top_k=2, line_format=None)


def dryrun():
    """
    Dry run.
    """
    f = Flow().load_config("flows/index.yml")
    with f:
        f.dry_run()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('choose between "index/search/dryrun" mode')
        exit(1)
    if sys.argv[1] == 'index':
        config()
        index()
    elif sys.argv[1] == 'search':
        config()
        search()
    else:
        raise NotImplementedError(f'unsupported mode {sys.argv[1]}')
