import unittest

#import pdb; pdb.set_trace()
# bit of a hack to check
# if 1) __builtin__ exists (for when using nosetests)
# or 2) if 'profile' has been injected by line_profiler
# if '__builtin__' not in dir() or not hasattr(__builtin__, 'profile'):
# def profile(func):
# def inner(*args, **kwargs):
# return func(*args, **kwargs)
# return inner

# memory profile
if 'profile' not in dir():
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
