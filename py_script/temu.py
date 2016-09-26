from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    print( x**1000000)

if __name__ == '__main__':
    pool=Pool(processes = 4)
    pool.apply_async(f, (2,3,4,5)) # runs in *only* one process
   # print(res)
