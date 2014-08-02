import codecs

# "Moby Words lists by Grady Ward"
# http://www.gutenberg.org/ebooks/3201
# SUMMARISED_FILE = "all_unique_words.txt"  # 500k approx
#CODEC = 'Windows-1252'

CODEC = 'utf-8'
SUMMARISED_FILE = "all_unique_words_wikipedia.txt"
# SUMMARISED_FILE = "all_unique_words_wikipedia_AA.txt"  # 4.8mil approx
# SUMMARISED_FILE = "all_unique_words_wikipedia_AABZ.txt"  # 8.5mil approx


def read_words(filename):
    # return words from filename using a generator
    try:
        with codecs.open(filename, 'r', CODEC) as f:
            for line_nbr, line in enumerate(f):
                items = line.strip().split()
                for item in items:
                    yield item
    except UnicodeDecodeError:
        print "UnicodeDecodeError for {} near line {} and word {}".format(filename, line_nbr, line)

readers = read_words(SUMMARISED_FILE)
