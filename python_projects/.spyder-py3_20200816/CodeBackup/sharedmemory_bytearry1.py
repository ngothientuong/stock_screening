# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

print()
print()
a = np.array([1, 1, 2, 3, 5, 8])

print("a.shape is: ", a.shape)
print("a.dtype is :", a.dtype)
print("a.nbyte is: ", a.nbytes)
from multiprocessing import shared_memory
shm = shared_memory.SharedMemory(name = "mySharedMemory", create=True, size=a.nbytes)
print("type shm.buf is: ", type(shm.buf))
# Now create a NumPy array backed by shared memory
b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
b[:] = a[:] # Copy the original data into shared memory
b;

# Note that b is now SharedMemory variable type to store 
# data. Any value is to store in shm SharedMemory variable shm
# will need to be inserted via b

print(b);
print(type(b))
print("type shm.name is ", type(shm.name));
print(type(shm.buf))
print(shm.buf[0], shm.buf[1], shm.buf[-1], shm.buf[2])


## Below is major example with a string

d = np.array("MY TOKEN")
print("d.shape is: ", d.shape)
print("d.dtype is :", d.dtype)
print("d.nbyte is: ", d.nbytes)

del d

c = 1;
print(type(c))


s = bytearray(4)
t = memoryview(s)
print("s is: ", s)
print("Type memory view is: ", type(memoryview))
s[1] = 7
print("t[1] = s[1] = ", t[1])

s = bytearray(b"ABCD")
print("type s is:", type(s)) 
print(s[0])
print(bytearray.decode(s))

mstring = "ABCD"
t = mstring.encode('utf-8')
# t is now b'ABCD'
print(t, "is class: ", type(t))
print("type bytearray(t) is" , bytearray(t))
print(bytearray.decode(bytearray(t)))


print()
print()
s = b"abcdefgh"
view = memoryview(s)
print(view[1])

limited = view[1:3]
print(limited)
print(bytes(view[1:3]))
print(memoryview(s)[4:])

