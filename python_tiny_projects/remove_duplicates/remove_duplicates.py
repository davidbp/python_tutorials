import os
from pathlib import Path
import hashlib
import ipyplot
import numpy as np
from PIL import Image
from tqdm import tqdm


path = './data_test'

file_list = os.walk(path)

file_hashes = dict()
for root,folders,files in tqdm(file_list):
    for file in files:
        path = Path(os.path.join(root,file))
        fhash = hashlib.md5(open(path,'rb').read()).hexdigest()
        
        if fhash in file_hashes:
            file_hashes[fhash].append(path)
        else:
            file_hashes[fhash] = [path]

duplicate_file_paths = [x[1] for x in file_hashes.items() if len(x[1])>1]

get_len = lambda x: len(x.stem)
for duplicates in tqdm(duplicate_file_paths):
    keep_index = np.argmin(list(map(get_len, duplicates)))
    for i, duplicate in enumerate(duplicates):
        if keep_index != i:
            print(f"removed file {duplicate}")
            os.remove(duplicate)
