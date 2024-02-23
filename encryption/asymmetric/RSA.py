# Core
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from encryption.utils import decode64, encode64


class RSAEncryption:
    @staticmethod
    # params: data/string , public_key/object => encrypted_data/string
    def encrypt(data, public_key):
        encrypted_data = public_key.encrypt(
            data.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decode64(encrypted_data)

    @staticmethod
    # params: data/string , private_key/object => decrypted_data/string
    def decrypt(data, private_key):
        decrypted_data = private_key.decrypt(
            encode64(data),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_data.decode('utf-8')
