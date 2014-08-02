from random import random


class MorrisCounter(object):
    counter = 0

    def add(self, *args):
        if random() < 1.0 / (2 ** self.counter):
            self.counter += 1

    def __len__(self):
        return 2 ** self.counter
