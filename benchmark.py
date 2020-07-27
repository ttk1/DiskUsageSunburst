#!/bin/env python

import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

# 参考: https://qiita.com/tag1216/items/db5adcf1ddcb67cfefc8


def getsize(path):
    try:
        return os.path.getsize(path)
    except:
        return 0


def task(v):
    return sum(getsize(os.path.join(v[0], filename)) for filename in v[2])


if __name__ == '__main__':
    '''
    実行時間:
    multithread << multiprocess < single thread
    '''

    # list only
    print('list only')
    start = time.time()
    print(len(list(os.walk('c:/'))))
    print('elapsed_time:{0:.2f} [sec]'.format(time.time() - start))
    print()

    # single thread
    print('single thread')
    start = time.time()
    print(sum(task(v) for v in os.walk('c:/')))
    print('elapsed_time:{0:.2f} [sec]'.format(time.time() - start))
    print()

    # multithread 4
    print('multithread 4')
    start = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(task, os.walk('c:/'))
    print(sum(results))
    print('elapsed_time:{0:.2f} [sec]'.format(time.time() - start))
    print()

    # multiprocess 4
    print('multiprocess 4')
    start = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(task, os.walk('c:/'))
    print(sum(results))
    print('elapsed_time:{0:.2f} [sec]'.format(time.time() - start))
    print()
