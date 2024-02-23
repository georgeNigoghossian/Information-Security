# Dev
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# params: void => private_key/object
def generateKeyPair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key


def exportPrivateKey(private_key, password=None):
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password) if password else serialization.NoEncryption()
    )
    return private_key_pem


def exportPublicKey(public_key):
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_key_pem


def importPrivateKey(pem_private_key, password=None):
    private_key = serialization.load_pem_private_key(
        pem_private_key,
        password=password
    )
    return private_key


def importPublicKey(pem_public_key):
    public_key = serialization.load_pem_public_key(
        pem_public_key
    )
    return public_key
