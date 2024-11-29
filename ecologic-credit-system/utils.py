from datetime import datetime
import ecdsa
from ecdsa import SigningKey
import hashlib

def get_time():
    """
    Return a string representing the current time in format "%Y-%m-%d %H:%M:%S.%f"
    :return: str
    """
    return str(datetime.now())


def str_to_time(s):
    """
    Convert a string into a datetime object.
    :param s: str
    :return:
    """
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")

def hash_str(sk):
    vk = sk.verifying_key.to_pem().hex()
    hash = hashlib.sha256(vk.encode()).hexdigest()
    return hash

def inv_sign(string):
    if string[0] == '+':
        return '-' + string[1:]
    elif string[0] == '-':
        return '+' + string[1:]