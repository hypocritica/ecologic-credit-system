"""
Configuration file for the blockchain. Initialization of various parameters.
"""

blockdepth = 2
blocksize = 2 ** blockdepth - 1  # Number of messages in a block

default_difficulty = 3

# the list of public keys ash for admins
import ecdsa
from ecdsa import SigningKey
import hashlib

sk_admin = SigningKey.generate(curve=ecdsa.SECP256k1)
vk = sk_admin.verifying_key.to_pem().hex()
hash = hashlib.sha256(vk.encode()).hexdigest()



admin_list = [hash] 
