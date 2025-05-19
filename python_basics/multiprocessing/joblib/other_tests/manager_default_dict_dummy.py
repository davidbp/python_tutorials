from multiprocessing import Pool
from multiprocessing.managers import BaseManager, DictProxy
from collections import defaultdict

class MyManager(BaseManager):
    pass

MyManager.register('defaultdict', defaultdict, DictProxy)

def test(k, multi_dict):
    multi_dict[k] += 1

if __name__ == '__main__':
    pool = Pool(processes=4)
    mgr = MyManager()
    mgr.start()
    multi_d = mgr.defaultdict(int)
    for k in 'mississippi':
        pool.apply_async(test, (k, multi_d))
    pool.close()
    pool.join()
    print multi_d.items()
