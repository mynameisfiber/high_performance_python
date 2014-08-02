def trailing_zeros(number):
    """
    Returns the 1-based index of the first bit set to 1 from the right side of a
    32bit integer
    >>> trailing_zeros(0)
    32
    >>> trailing_zeros(0b1000)
    4
    >>> trailing_zeros(0b10000000)
    8
    """
    if not number:
        return 32
    index = 0
    while (number >> index) & 1 == 0:
        index += 1
    return index + 1
