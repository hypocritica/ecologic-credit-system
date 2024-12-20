from transaction import Transaction
from ecdsa import SigningKey
import binascii

Message = "test"
Value = "-10"
Destination = "daa1a9d79ed50144844d07276d282c1cf3227545f042f5e83f5d721ac521124c"
Date = "2024-11-29 10:09:04.885948"
Verification_Key ="2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d456b77457759484b6f5a497a6a3043415159494b6f5a497a6a3044415145444d674145706a34305a4537516a463636505a587638664762676e344749464b7064784b6f6d717437375673480a4f48476e742f47544f72774f72787238716e4674325755690a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d0a"
Author = "daa1a9d79ed50144844d07276d282c1cf3227545f042f5e83f5d721ac521124c"
Signature = "5506c6e1f9e73d63aca0b4ef24f13d9b2be88d030cacb77e58b493de99818d6a8d386e307c8a1d6d336be7f7e3ad8b12"

t = Transaction(Message, Value, Destination, Date, Signature ,Verification_Key, Author)

print(t.verify())

print(len(Destination))

sk = SigningKey.generate()

sk_string = binascii.hexlify(sk.to_string()).decode('utf-8')

sk_bytes = binascii.unhexlify(sk_string.encode('utf-8'))
sk_restored = SigningKey.from_string(sk_bytes)

print(sk_string)

print(sk_restored == sk)

