import json

from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption
from encryption.asymmetric.key_pair_generator import importPrivateKey
from university_project.Client.request_templates.requests_functions import send_marks
from encryption.digital_signature.DigitalSignature import DigitalSignature


def main():
    server_url = f'127.0.0.1:8000'

    # get the token from the file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    token = lines[1].split(":")[1].strip()
    file.close()

    # get client session key
    file = open("./client_info/task3_session_key.txt", "r")
    lines = file.readlines()
    session_key = lines[0].split(":")[1].strip()
    file.close()

    # get client private key
    file = open("./client_info/task3_client_private_key.txt", "r")
    lines = file.read()
    file.close()
    private_key = importPrivateKey(lines.encode('utf-8'))

    # initiate students marks
    marks = {
        'jogo': '100',
        'Goku': '99'
    }

    # generate IV to encrypt data than mac from encrypted_data
    iv = generateIv()
    encrypted_data = AESEncryption.encrypt(json.dumps(marks), session_key, iv)

    # generate Digital Signature
    digital_signature = DigitalSignature.createDigitalSignature(encrypted_data, private_key)

    # call the complete signUp function to start connection with the socket
    res, status = send_marks(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "iv": iv,
            "encrypted_data": encrypted_data,
            "digital_signature": digital_signature
        },
    )

    # decrypt the returned response
    res = json.loads(res)
    decrypted_message = AESEncryption.decrypt(res.get("encrypted_message"), session_key, res.get("iv"))

    print(decrypted_message)


if __name__ == "__main__":
    main()
