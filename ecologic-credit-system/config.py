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

sk_admin = SigningKey.generate(curve=ecdsa.SECP256k1)
hash = hash_str(sk_admin)
admin_list = [hash] 

show_mempool = True