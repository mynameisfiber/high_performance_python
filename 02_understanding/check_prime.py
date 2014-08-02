import math


def check_prime(number):
    sqrt_number = math.sqrt(number)
    number_float = float(number)
    for i in xrange(2, int(sqrt_number) + 1):
        if (number_float / i).is_integer():
            return False
    return True

if __name__ == "__main__":
    print "check_prime(10000000) = ", check_prime(10000000)
    print "check_prime(10000019) = ", check_prime(10000019)
