import fnmatch
import itertools
import codecs
import os
import glob

# Convert wikipedia files into a unique words list
# of course this file won't fit into RAM...

matches = []
WIKIPEDIA_RAW_DIR = "/media/ian/data/wikipedia_data_dump/extracted/"
# ["/media/ian/data/wikipedia_data_dump/extracted/AA", "/media/ian/data/wikipedia_data_dump/extracted/AB"]  # off of western digital
WIKIPEDIA_FILES_ROOTS = glob.glob(os.path.join(
    WIKIPEDIA_RAW_DIR, "A*")) + glob.glob(os.path.join(WIKIPEDIA_RAW_DIR, "B*"))
print "Working from raw roots:", WIKIPEDIA_FILES_ROOTS
for wikipedia_files_root in WIKIPEDIA_FILES_ROOTS:
    for root, dirnames, filenames in os.walk(wikipedia_files_root):
        for filename in fnmatch.filter(filenames, 'wiki*'):
            matches.append(os.path.join(root, filename))
SUMMARISED_FILE = "all_unique_words_wikipedia_AABZ.txt"
LONG_FILES = matches
print "Using e.g. {} of {}".format(len(LONG_FILES), LONG_FILES[:10])


def read_words(filename):
    # return words from filename using a generator
    try:
        with codecs.open(filename, 'r', 'utf-8') as f:
            for line_nbr, line in enumerate(f):
                items = line.strip().split()
                for item in items:
                    yield item
    except UnicodeDecodeError:
        print "UnicodeDecodeError for {} near line {} and word {}".format(filename, line_nbr, line)

readers = itertools.chain(*(read_words(lf) for lf in LONG_FILES))

if __name__ == "__main__":
    words_set = set(readers)
    print "Summarising input files into one output set of {} words".format(len(words_set))
    with codecs.open(SUMMARISED_FILE, 'w', 'utf-8') as f:
        for word in words_set:
            f.write(word + "\n")
