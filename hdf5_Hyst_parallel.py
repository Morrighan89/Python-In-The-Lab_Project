import glob, os, sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

def f2(x):
    return x*x


if __name__ == '__main__':
    info('main line')
    y=[1,2,3]
    p = multiprocessing.Process(target=f2, args=1)
    p.start()
    p.join()
