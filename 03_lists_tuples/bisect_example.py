import bisect
import random


def find_closest(haystack, needle):
    # bisect.bisect_left will return the first value in the haystack that is greater
    # than or equal to the needle
    i = bisect.bisect_left(haystack, needle)
    if i == len(haystack):
        return i - 1
    elif haystack[i] == needle:
        return i
    elif i > 0:
        j = i - 1
        # since we know value is larger than needle (and vice versa for the
        # value at j), we don't need to use absolute values here
        if haystack[i] - needle > needle - haystack[j]:
            return j
    return i

if __name__ == "__main__":
    important_numbers = []
    for i in xrange(10):
        new_number = random.randint(0, 1000)
        bisect.insort(important_numbers, new_number)

    # important_numbers will be already in order because we inserted new elements
    # with bisect.insort
    print "Haystack: ", important_numbers

    closest_index = find_closest(important_numbers, -250)
    print "Closest value to -250: ", important_numbers[closest_index]

    closest_index = find_closest(important_numbers, 500)
    print "Closest value to 500: ", important_numbers[closest_index]

    closest_index = find_closest(important_numbers, 1100)
    print "Closest value to 1100: ", important_numbers[closest_index]
