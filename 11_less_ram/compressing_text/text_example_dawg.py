import time
import timeit
import text_example
import memory_profiler
import dawg

if __name__ == "__main__":
    print "RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0])
    # avoid building a temporary list of words in Python, store directly in the
    # DAWG
    t1 = time.time()
    words_dawg = dawg.DAWG(text_example.readers)
    t2 = time.time()
    print "RAM after creating dawg {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1)

    assert u'Zwiebel' in words_dawg
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in words_dawg",
                                  setup="from __main__ import words_dawg",
                                  number=1,
                                  repeat=10000))
    print "Summed time to lookup word {:0.4f}s".format(time_cost)
