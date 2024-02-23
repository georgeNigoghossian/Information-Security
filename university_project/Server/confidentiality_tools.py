from Cryptodome.PublicKey import RSA

from Authentication.models import ServerKeys

from encryption.asymmetric.key_pair_generator import generateKeyPair, exportPrivateKey


def generate_server_keys():
    # private_key = RSA.generate(2048)
    # public_key = private_key.publickey()
    # with open("server_private_key.pem", "wb") as f:
    #     f.write(private_key.export_key('PEM'))
    # with open("server_public_key.pem", "wb") as f:
    #     f.write(public_key.export_key('PEM'))
    # data_to_insert = ServerKeys(
    #   '1',
    #   public_key.export_key('PEM').decode('utf-8'),
    #   private_key.export_key('PEM').decode('utf-8')
    # )
    # data_to_insert.save()

    private_key = generateKeyPair()
    insert_data = ServerKeys('1', '', exportPrivateKey(private_key).decode('utf-8'))
    insert_data.save()
    return True
