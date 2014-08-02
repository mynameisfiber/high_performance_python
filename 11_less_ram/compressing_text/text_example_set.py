import time
import timeit
import text_example
import memory_profiler

if __name__ == "__main__":
    print "RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0])
    # load the words directly into the set
    t1 = time.time()
    words_set = set(text_example.readers)
    t2 = time.time()
    print "RAM after creating set {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1)
    print "The set contains {} words".format(len(words_set))

    assert u'Zwiebel' in words_set
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in words_set",
                                  setup="from __main__ import words_set",
                                  number=1,
                                  repeat=10000))
    print "Summed time to lookup word {:0.4f}s".format(time_cost)
