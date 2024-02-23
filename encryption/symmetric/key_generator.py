# Core
import hashlib
import secrets

# Dev
from encryption.utils import decode64


# params: value/string => key/string
def generateAESKey(value):
    number_bytes = value.encode('utf-8')

    # Hash the number bytes using SHA-256
    hash_object = hashlib.sha256()
    hash_object.update(number_bytes)
    key_bytes = hash_object.digest()

    # Take the first 16 byte
    key_16_bytes = key_bytes[:16]

    # Convert the key bytes to a hexadecimal string
    key_hex = key_16_bytes.hex()

    return key_hex


# params: void => iv/string
def generateIv():
    iv = secrets.token_bytes(16)
    iv = decode64(iv)
    return iv


# params: void => session_key/string
def generateSessionKey():
    session_key = secrets.token_bytes(16)
    session_key = decode64(session_key)
    return session_key
