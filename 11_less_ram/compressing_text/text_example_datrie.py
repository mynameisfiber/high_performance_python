import time
import timeit
import itertools
import text_example
import memory_profiler
import datrie

if __name__ == "__main__":
    print "RAM at start {:0.1f}MiB".format(memory_profiler.memory_usage()[0])
    # avoid building a temporary list of words in Python, store directly in the
    # Trie
    t0 = time.time()
    chars = set()
    for word in text_example.readers:
        chars.update(word)
    trie = datrie.BaseTrie(chars)

    t1 = time.time()
    print "Created a trie with a dictionary of {} characters in {:0.1f}s".format(len(chars), t1 - t0)
    readers = text_example.read_words(text_example.SUMMARISED_FILE)
    for word in readers:
        trie[word] = 0
    t2 = time.time()
    print "RAM after creating trie {:0.1f}MiB, took {:0.1f}s".format(memory_profiler.memory_usage()[0], t2 - t1)
    print "The trie contains {} words".format(len(trie))

    assert u'Zwiebel' in trie
    time_cost = sum(timeit.repeat(stmt="u'Zwiebel' in trie",
                                  setup="from __main__ import trie",
                                  number=1,
                                  repeat=10000))
    print "Summed time to lookup word {:0.4f}s".format(time_cost)
