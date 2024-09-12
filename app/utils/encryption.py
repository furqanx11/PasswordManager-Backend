from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()  # You can use a password if needed
        ))

    public_key = private_key.public_key()
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

generate_rsa_keys()



def load_public_key():
    with open("public_key.pem", "rb") as key_file:
        public_key = load_pem_public_key(key_file.read(), backend=default_backend())
    return public_key


def load_private_key():
    with open("private_key.pem", "rb") as key_file:
        private_key = load_pem_private_key(key_file.read(), password=None, backend=default_backend())
    return private_key



def encrypt_with_rsa(public_key, plaintext):
    ciphertext = public_key.encrypt(
        plaintext.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_with_rsa(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

ciphertext = encrypt_with_rsa(load_public_key(), "Hurera Mujeeb")
print(ciphertext)
plaintext = decrypt_with_rsa(load_private_key(), ciphertext)

print(plaintext)


