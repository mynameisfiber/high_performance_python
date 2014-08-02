import time
import timeit
import text_example
import memory_profiler
import marisa_trie

if __name__ == "__main__":
    print "RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0])
    # avoid building a temporary list of words in Python, store directly in the
    # Trie
    t1 = time.time()
    words_trie = marisa_trie.Trie(text_example.readers)
    t2 = time.time()
    print "RAM after creating trie {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1)
    print "The trie contains {} words".format(len(words_trie))

    assert u'Zwiebel' in words_trie
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in words_trie",
                                  setup="from __main__ import words_trie",
                                  number=1,
                                  repeat=10000))
    print "Summed time to lookup word {:0.4f}s".format(time_cost)
