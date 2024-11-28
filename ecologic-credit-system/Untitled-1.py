import re


pattern = r"^[^:]+(?:\s+[^:]+)*\s*:\s*[-+][0-9]+$"

def test():
    string = None
    while string!='end':
        string = input()
        print(re.match(pattern, string))

#test()

print(int('+43'))
print(int('-31'))

print(len('8c7a2776446cec5519df357acbb06e5af2acefa6ccbf9f2015f3482aa6c00cb2'))

import ecdsa

# Générer une clé privée
sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

# Obtenir la clé publique à partir de la clé privée
vk = sk.get_verifying_key()

# Convertir la clé publique en format hexadécimal
public_key_hex = vk.to_string().hex()

# Afficher la clé publique
print(f"Clé publique (hexadécimale) : {public_key_hex}")