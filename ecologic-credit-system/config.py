"""
Configuration file for the blockchain. Initialization of various parameters.
"""

blockdepth = 2
blocksize = 2 ** blockdepth - 1  # Number of messages in a block

default_difficulty = 3

# the list of public keys ash for admins
import ecdsa
from ecdsa import SigningKey
from utils import hash_str
import binascii

sk_string = "a2b461ce2e0f2af25163413a06f3c0eb8ef9081cb556192e"
sk_bytes = binascii.unhexlify(sk_string.encode('utf-8'))
sk_restored = SigningKey.from_string(sk_bytes)
hash = hash_str(sk_restored)

admin_list = [hash] 

show_mempool = True