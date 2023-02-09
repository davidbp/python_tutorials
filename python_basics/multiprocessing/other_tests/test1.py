
from multiprocessing import Pool

import time

work = (["A", 5], ["B", 2], ["C", 1], ["D", 3])


def work_log(work_data):
    print(" Process %s waiting %s seconds" % (work_data[0], work_data[1]))
    time.sleep(int(work_data[1]))
    print(" Process %s Finished." % work_data[0])
    return int(work_data[1])


def pool_handler():
    p = Pool(2)
    return p.map(work_log, work)


if __name__ == '__main__':
    result = pool_handler()
    print('type(p.map(...)) is ', type(result))
    print('p.map(...) is ', result)
