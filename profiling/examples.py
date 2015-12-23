import hashlib


class Crypto(object):
    def __init__(self, algorithm):
        self.hash_algorithm = algorithm

    def hash(self, s):
        h = getattr(hashlib, self.hash_algorithm)()
        h.update(s)
        return h.digest()


def hash(s):
    h = hashlib.sha512()
    h.update(s)
    return h.digest()
