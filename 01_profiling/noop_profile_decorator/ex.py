import unittest

#import pdb; pdb.set_trace()
# if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'):
# def profile(func):
# def inner(*args, **kwargs):
# return func(*args, **kwargs)
# return inner

try:
    profile
except NameError:
    def profile(func):
        def inner(*args, **kwargs):
            return func(*args, **kwargs)
        return inner


@profile
def some_fn(nbr):
    return nbr * 2


class TestCase(unittest.TestCase):

    def test(self):
        result = some_fn(2)
        self.assertEquals(result, 4)


if __name__ == "__main__":
    print "do some work:", some_fn(2)
    # unittest.main()
