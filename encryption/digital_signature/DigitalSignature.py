from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

from encryption.utils import decode64, encode64


class DigitalSignature:
    @staticmethod
    # params: encrypted_data/string , private_key/object => signature/string
    def createDigitalSignature(encrypted_data, private_key):
        signature = private_key.sign(
            encode64(encrypted_data),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return decode64(signature)

    @staticmethod
    # params: signature/string , encrypted_data/string , public_key/object => boolean
    def verifyDigitalSignature(signature, encrypted_data, public_key):
        try:
            public_key.verify(
                encode64(signature),
                encode64(encrypted_data),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
