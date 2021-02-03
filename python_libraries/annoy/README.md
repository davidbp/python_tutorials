

## Approximate K Nearest Neighbor (AKNN)




- ANNOY: Spottify implementation


  - Github repository: https://github.com/spotify/annoy

    

### ANNOY

Key points from the library:

- It has the ability to **use static files as indexes**: this means you can **share index across processes**. 
- it tries to minimize memory footprint so the indexes are quite small

- Allows [Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance), [Manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry), [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity), [Hamming distance](https://en.wikipedia.org/wiki/Hamming_distance), or [Dot (Inner) Product distance](https://en.wikipedia.org/wiki/Dot_product)
- Cosine distance is equivalent to Euclidean distance of normalized vectors = sqrt(2-2*cos(u, v))
- Works better if you don't have too many dimensions (like <100) but seems to perform surprisingly well even up to 1,000 dimensions
- Small memory usage
- Lets you share memory between multiple processes
- Index creation is separate from lookup (in particular you can not add more items once the tree has been created)
- Native Python support, tested with 2.7, 3.6, and 3.7.
- Build index on disk to enable indexing big datasets that won't fit into memory (contributed by [Rene Hollander](https://github.com/ReneHollander))



## Full Python API

- `AnnoyIndex(f, metric)` returns a new index that's read-write and stores vector of `f` dimensions. Metric can be `"angular"`, `"euclidean"`, `"manhattan"`, `"hamming"`, or `"dot"`.
- `a.add_item(i, v)` adds item `i` (any nonnegative integer) with vector `v`. Note that it will allocate memory for `max(i)+1` items.
- `a.build(n_trees, n_jobs=-1)` builds a forest of `n_trees` trees. More trees gives higher precision when querying. After calling `build`, no more items can be added. `n_jobs` specifies the number of threads used to build the trees. `n_jobs=-1` uses all available CPU cores.
- `a.save(fn, prefault=False)` saves the index to disk and loads it (see next function). After saving, no more items can be added.
- `a.load(fn, prefault=False)` loads (mmaps) an index from disk. If prefault is set to True, it will pre-read the entire file into memory (using mmap with MAP_POPULATE). Default is False.
- `a.unload()` unloads.
- `a.get_nns_by_item(i, n, search_k=-1, include_distances=False)` returns the `n` closest items. During the query it will inspect up to `search_k` nodes which defaults to `n_trees * n` if not provided. `search_k`gives you a run-time tradeoff between better accuracy and speed. If you set `include_distances` to `True`, it will return a 2 element tuple with two lists in it: the second one containing all corresponding distances.
- `a.get_nns_by_vector(v, n, search_k=-1, include_distances=False)` same but query by vector `v`.
- `a.get_item_vector(i)` returns the vector for item `i` that was previously added.
- `a.get_distance(i, j)` returns the distance between items `i` and `j`. NOTE: this used to return the *squared* distance, but has been changed as of Aug 2016.
- `a.get_n_items()` returns the number of items in the index.
- `a.get_n_trees()` returns the number of trees in the index.
- `a.on_disk_build(fn)` prepares annoy to build the index in the specified file instead of RAM (execute before adding items, no need to save after build)
- `a.set_seed(seed)` will initialize the random number generator with the given seed. Only used for building up the tree, i. e. only necessary to pass this before adding the items. Will have no effect after calling a.build(n_trees) or a.load(fn).

