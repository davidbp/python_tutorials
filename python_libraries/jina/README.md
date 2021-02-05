

To run a hello word example in Jina you can type:

```
jina hello-world
```

After some computation you should be prompted with:

![result_hello_word](images/result_hello_word.png)



This script contains different options that can be passed as an argument

```
jina hello-world --help
```

```

usage: jina hello-world [-h] [--workdir] [--logserver] [--logserver-config]
                        [--download-proxy] [--shards] [--parallel]
                        [--uses-index] [--index-data-url] [--index-batch-size]
                        [--uses-query] [--query-data-url] [--query-batch-size]
                        [--num-query] [--top-k]

Start the hello-world demo, a simple end2end image index and search demo without any extra dependencies.

⚙️  Optional Arguments
  -h, --help           show this help message and exit

⚙️  General Arguments
  --workdir            the workdir for hello-world demo, all data, indices,
                       shards and outputs will be saved there (type: str;
                       default: 39b6f6ee259511ebad42787b8ab3f5de)
  --logserver          start a log server for the dashboard (default:
                       disabled, use "--logserver" to enable it)
  --logserver-config   the yaml config of the log server (type: str;
                       default: /Users/davidbuchaca1/anaconda3/envs/py3_7/lib/
                       python3.7/site-
                       packages/jina/resources/logserver.default.yml)
  --download-proxy     specify the proxy when downloading sample data
                       (type: str; default: None)

⚙️  Scalability Arguments
  --shards             number of shards when index and query (type: int;
                       default: 2)
  --parallel           number of parallel when index and query (type: int;
                       default: 2)

⚙️  Index Arguments
  --uses-index         the yaml path of the index flow (type: str;
                       default: /Users/davidbuchaca1/anaconda3/envs/py3_7/lib/
                       python3.7/site-
                       packages/jina/resources/helloworld.flow.index.yml)
  --index-data-url     the url of index data (should be in idx3-ubyte.gz
                       format) (type: str; default: http://fashion-
                       mnist.s3-website.eu-central-1.amazonaws.com/train-
                       images-idx3-ubyte.gz)
  --index-batch-size   the batch size in indexing (type: int; default:
                       1024)

⚙️  Query Arguments
  --uses-query         the yaml path of the query flow (type: str;
                       default: /Users/davidbuchaca1/anaconda3/envs/py3_7/lib/
                       python3.7/site-
                       packages/jina/resources/helloworld.flow.query.yml)
  --query-data-url     the url of query data (should be in idx3-ubyte.gz
                       format) (type: str; default: http://fashion-
                       mnist.s3-website.eu-
                       central-1.amazonaws.com/t10k-images-idx3-ubyte.gz)
  --query-batch-size   the batch size in searching (type: int; default:
                       32)
  --num-query          number of queries to visualize (type: int; default:
                       128)
  --top-k              top-k results to retrieve and visualize (type: int;
                       default: 50)


```





