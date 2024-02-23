# Core
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

# Dev
from encryption.symmetric.key_generator import generateIv
from encryption.mac.MAC import Mac
from encryption.utils import encode64, decode64


class AESEncryption:
    @staticmethod
    # params: data/string , key/string , iv/string => {ct/string}
    def encrypt(data, key, iv):
        # convert key & iv to byte
        key = key.encode('utf-8')
        iv = encode64(iv)

        # encrypt the data using the key & iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

        # convert to string to send
        encrypted_data = decode64(ct_bytes)

        # return the encrypted_data
        return encrypted_data

    @staticmethod
    # params: data/string , key/string , iv/string => data/string
    def decrypt(data, key, iv):
        # convert key & iv to byte
        key = key.encode('utf-8')
        iv = encode64(iv)

        # decrypt the data using key & iv
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ct_bytes = encode64(data)
        pt_bytes = unpad(cipher.decrypt(ct_bytes), AES.block_size)
        decrypted_data = pt_bytes.decode('utf-8')

        # return the decrypted data
        return decrypted_data
