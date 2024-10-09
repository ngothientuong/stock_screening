# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 10:48:23 2020

@author: Owner
"""
import first_module
from config import tda_real_username
from multiprocessing import shared_memory
import numpy as np

existing_shm = shared_memory.SharedMemory(name='mySharedMemory')
# Note that a.shape is (6,) and a.dtype is np.int64 in this example
c = np.ndarray((6,), dtype=np.int32, buffer=existing_shm.buf)
print(type(c))
print('arry c is: ', c)

