import hashlib


def get_hash_args():
    return ('that dog runs fast.',)


def hash(s):
    h = hashlib.sha512()
    h.update(s)
    return h.digest()
