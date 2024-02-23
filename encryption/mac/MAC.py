from Cryptodome.Hash import HMAC, SHA256
from encryption.utils import encode64, decode64


class Mac:
    @staticmethod
    # params: key/string , encrypted_data/string , iv/string => mac/string
    def generateMac(key, encrypted_data, iv):

        # convert key & iv & data to byte
        key = key.encode('utf-8')
        iv = encode64(iv)
        encrypted_data = encode64(encrypted_data)

        # generate the mac by key + (data + iv)
        hmac_obj = HMAC.new(key, digestmod=SHA256)
        hmac_obj.update(iv + encrypted_data)
        mac = hmac_obj.digest()

        # return the mac
        return decode64(mac)

    @staticmethod
    # params: key/string , encrypted_data/string , iv/string , mac/string => boolean
    def verifyMac(key, mac, encrypted_data, iv):

        # convert key & iv & data to byte
        key = key.encode('utf-8')
        iv = encode64(iv)
        encrypted_data = encode64(encrypted_data)
        mac = encode64(mac)

        # generate the mac again to verify
        hmac_obj = HMAC.new(key, digestmod=SHA256)
        hmac_obj.update(iv + encrypted_data)

        # return the verify result
        try:
            hmac_obj.verify(mac)
            return True
        except ValueError:
            return False
