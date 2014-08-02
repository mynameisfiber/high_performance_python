from itertools import islice


def index_sequence(key, mask=0b111, PERTURB_SHIFT=5):
    perturb = hash(key)
    i = perturb & mask
    yield i
    while True:
        i = ((i << 2) + i + perturb + 1)
        perturb >>= PERTURB_SHIFT
        yield i & mask


class ForceHash(object):

    def __init__(self, force_hash):
        self.force_hash = force_hash

    def __hash__(self):
        return self.force_hash

    def __str__(self):
        return "0b{:08b}".format(self.force_hash)


def sample_probe(force_hash, num_samples=10):
    probe_values = index_sequence(force_hash)
    indexes = islice(probe_values, num_samples)
    print "First {} samples for hash {: >10}: {}".format(
        num_samples,
        force_hash,
        list(indexes)
    )


if __name__ == "__main__":
    sample_probe(ForceHash(0b00000111))
    sample_probe(ForceHash(0b11100111))
    sample_probe(ForceHash(0b01110111))
    sample_probe(ForceHash(0b01110001))
    sample_probe(ForceHash(0b01110000))
