class Point(object):

    def __init__(self, x, y):
        self.x, self.y = x, y


class PointHash(object):

    def __init__(self, x, y):
        self.x, self.y = x, y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


if __name__ == "__main__":
    print "Test with default hash function"
    p1 = Point(1, 1)
    p2 = Point(1, 1)
    points = set([p1, p2])
    print "Contents of set([p1, p2]): ", points
    print "Point(1, 1) in set([p1, p2]) = ", (Point(1, 1) in points)

    print "Test with custom hash function"
    p1 = PointHash(1, 1)
    p2 = PointHash(1, 1)
    points = set([p1, p2])
    print "Contents of set([p1, p2]): ", points
    print "Point(1, 1) in set([p1, p2]) = ", (PointHash(1, 1) in points)
