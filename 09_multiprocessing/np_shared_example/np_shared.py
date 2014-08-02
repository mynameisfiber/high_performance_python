import os
import multiprocessing
from collections import Counter
import ctypes
import numpy as np
from prettytable import PrettyTable

# http://stackoverflow.com/questions/5549190/is-shared-readonly-data-copied-to-different-processes-for-python-multiprocessing/5550156#5550156
# from user pv
# http://stackoverflow.com/users/108184/pv

# notes from alex martelli on why this is hard in pure python
# http://stackoverflow.com/questions/1268252/python-possible-to-share-in-memory-data-between-2-separate-processes
# note on connecting back from a subprocess to a later developed bit of shared
# memory
# http://stackoverflow.com/questions/7419159/giving-access-to-shared-memory-after-child-processes-have-already-started

# for reporting we can see size and vsize:
# $ ps -A -o pid,size,vsize,cmd | grep np_shared
# using pmap on the parent and children we can see shared data
# $ pmap -x 25100  # look at shared RAM used by forked children or parent
# report free RAM
# $ free

#SIZE_A, SIZE_B = 10000, 100
#SIZE_A, SIZE_B = 10000, 1000
# SIZE_A, SIZE_B = 10000, 40000  # 3.2GB (3.2e9 bytes)  # GOOD DEMO
SIZE_A, SIZE_B = 10000, 80000  # 6.2GB - starts to use swap via htop


def worker_fn(idx):
    """Do some work on the shared np array on row idx"""
    # confirm that no other process has modified this value already
    assert main_nparray[idx, 0] == DEFAULT_VALUE
    # inside the subprocess print the PID and id of the array
    # to check we don't have a copy
    if idx % 1000 == 0:
        print " {}: with idx {}\n  id of local_nparray_in_process is {} in PID {}"\
            .format(worker_fn.__name__, idx, id(main_nparray), os.getpid())
    # we can do any work on the array, here we set every item in this row to
    # have the value of the process id for this process
    main_nparray[idx, :] = os.getpid()


if __name__ == '__main__':
    DEFAULT_VALUE = 42
    NBR_OF_PROCESSES = 4

    # create a block of bytes, reshape into a local numpy array
    NBR_ITEMS_IN_ARRAY = SIZE_A * SIZE_B
    shared_array_base = multiprocessing.Array(
        ctypes.c_double, NBR_ITEMS_IN_ARRAY, lock=False)
    main_nparray = np.frombuffer(shared_array_base, dtype=ctypes.c_double)
    main_nparray = main_nparray.reshape(SIZE_A, SIZE_B)
    # Assert no copy was made
    assert main_nparray.base.base is shared_array_base
    print "Created shared array with {:,} nbytes".format(main_nparray.nbytes)
    print "Shared array id is {} in PID {}".format(id(main_nparray), os.getpid())
    print "Starting with an array of 0 values:"
    print main_nparray
    print

    # Modify the data via our local numpy array
    main_nparray.fill(DEFAULT_VALUE)
    print "Original array filled with value {}:".format(DEFAULT_VALUE)
    print main_nparray

    raw_input("Press a key to start workers using multiprocessing...")
    print

    # create a pool of processes that will share the memory block
    # of the global numpy array, share the reference to the underlying
    # block of data so we can build a numpy array wrapper in the new processes
    pool = multiprocessing.Pool(processes=NBR_OF_PROCESSES)
    # perform a map where each row index is passed as a parameter to the
    # worker_fn
    pool.map(worker_fn, xrange(SIZE_A))

    print
    print "The default value has been over-written with worker_fn's result:"
    print main_nparray
    print
    print "Verification - extracting unique values from {:,} items\nin the numpy array (this might be slow)...".format(NBR_ITEMS_IN_ARRAY)
    # main_nparray.flat iterates over the contents of the array, it doesn't
    # make a copy
    counter = Counter(main_nparray.flat)
    print "Unique values in main_nparray:"
    tbl = PrettyTable(["PID", "Count"])
    for pid, count in counter.items():
        tbl.add_row([pid, count])
    print tbl

    total_items_set_in_array = sum(counter.values())

    # check that we have set every item in the array away from DEFAULT_VALUE
    assert DEFAULT_VALUE not in counter.keys()
    # check that we have accounted for every item in the array
    assert total_items_set_in_array == NBR_ITEMS_IN_ARRAY
    # check that we have NBR_OF_PROCESSES of unique keys to confirm that every
    # process did some of the work
    assert len(counter) == NBR_OF_PROCESSES

    raw_input("Press a key to exit...")
