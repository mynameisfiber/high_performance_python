import multiprocessing as mp
from multiprocessing import Value
import array
import os
import time
import memory_profiler

init = " " * int(1e10)
arr = array.array('c', init)


def f(a, v):
    print "running", os.getpid(), len(a)
    print "in process", memory_profiler.memory_usage()
    #a[0] = 'x'
    print "did arr get changed in process?", a[:5]
    v.value = len(a)
    time.sleep(5)

value = Value('L')
print value
print "before making process", memory_profiler.memory_usage()
p = mp.Process(target=f, args=(arr, value))
print "after making process", memory_profiler.memory_usage()
p.start()
print "after making process 2", memory_profiler.memory_usage()
p.join()  # a sleep would work but this is neater
print "Value is:", value.value
print "did arr get changed?", arr[:5]
