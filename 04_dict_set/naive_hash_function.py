class City(str):

    def __hash__(self):
        return ord(self[0])

if __name__ == "__main__":
    print "Adding Rome, San Francisco, New York and Barcelona to a set.  New York and Barcenlona will collide!"
    data = {
        City("Rome"),
        City("San Francisco"),
        City("New York"),
        City("Barcelona"),
    }
