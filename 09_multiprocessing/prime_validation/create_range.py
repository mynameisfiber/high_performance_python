"""Create a list of (from, to) ranges for parallelizing tasks"""
import unittest


def create(range_from, range_to, chunks):
    partial_range_length = (range_to - range_from) / float(chunks)
    lower_ranges = range(range_from, range_to, int(partial_range_length))
    # keep the first lower_range (it might be just 2), make sure each
    # subsequent value is odd
    lrs = [lower_ranges[0]]
    for lower_range in lower_ranges[1:]:
        if lower_range % 2 == 0:
            lrs.append(lower_range + 1)
        else:
            lrs.append(lower_range)
    lower_ranges = lrs
    if len(lower_ranges) > chunks:
        lower_ranges.pop()
    assert len(lower_ranges) == chunks
    ranges = zip(
        lower_ranges, lower_ranges[1:]) + [(lower_ranges[-1], range_to)]
    return ranges


# def chunk(start, end, chunks):
    # Micha's variant
    # create a delta
    #dx = int((end - start) / float(chunks))
    # 1 if even, 0 if odd
    #dx_even = (dx % 2 == 0)
    #x = start
    # while x < end:
    # offset used as a binary XOR takes care of the fact that
    # odd + odd = even
    # even + even = even
    #offset = not((x % 2 == 0) ^ dx_even)
    #end_for_step = min(end, x + dx + int(offset))
    #last = (x, end_for_step)
    # yield last
    #x = last[1]


# def create(start, end, chunks):
    # return [item for item in chunk(start, end, chunks)]


class test(unittest.TestCase):

    def test1(self):
        range_from = 2
        range_to = 11
        chunks = 2
        expected = [(2, 7), (7, 11)]
        ranges = create(range_from, range_to, chunks)
        self.assertEqual(expected, ranges)

    def test2(self):
        range_from = 1
        range_to = 31
        chunks = 3
        expected = [(1, 11), (11, 21), (21, 31)]
        ranges = create(range_from, range_to, chunks)
        self.assertEqual(expected, ranges)

    def test3(self):
        range_from = 1
        range_to = 31
        chunks = 4
        # expected = [(1, 9), (9, 15), (15, 23), (23, 31)]  # ian's original
        expected = [(1, 9), (9, 17), (17, 25), (25, 31)]
        ranges = create(range_from, range_to, chunks)
        self.assertEqual(expected, ranges)
