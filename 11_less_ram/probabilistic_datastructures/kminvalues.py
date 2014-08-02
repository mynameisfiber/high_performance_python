import mmh3
from blist import sortedset


class KMinValues(object):

    def __init__(self, num_hashes):
        self.num_hashes = num_hashes
        self.data = sortedset()

    def add(self, item):
        item_hash = mmh3.hash(item)
        self.data.add(item_hash)
        if len(self.data) > self.num_hashes:
            self.data.pop()

    def __len__(self):
        if len(self.data) <= 2:
            return 0
        return (self.num_hashes - 1) * (2 ** 32 - 1) / \
            float(self.data[-2] + 2 ** 31 - 1)
