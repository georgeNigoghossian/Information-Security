# Core
import json

# Dev
from encryption.asymmetric.key_pair_generator import generateKeyPair, exportPrivateKey, exportPublicKey, importPublicKey
from encryption.symmetric.key_generator import generateSessionKey
from encryption.asymmetric.RSA import RSAEncryption
from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption
from university_project.Client.request_templates.requests_functions import key_exchange, send_session_key_to_server, send_project


def handshaking(token):
    server_url = f'127.0.0.1:8000'

    # generate client private/public keys
    client_private_key = generateKeyPair()

    # save private key in the client info
    file = open("./client_info/task3_client_private_key.txt", "w")
    file.truncate()
    file.writelines([exportPrivateKey(client_private_key).decode('utf-8')])
    file.close()

    # call the complete signUp function to start connection with the socket
    res, status = key_exchange(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "client_public_key": exportPublicKey(client_private_key.public_key()).decode('utf-8')
        },
    )

    # check if the exchange public key success
    if status != 200:
        print("exchange public keys Incomplete!!!")
        return

    print("Exchanging public keys completed successfully" + "\n")

    # get the server public key & save it in the client file
    res = json.loads(res)
    file = open("./client_info/task3_server_public_key.txt", "w")
    file.truncate()
    file.writelines([res.get("server_public_key")])
    file.close()

    # generate session key & encrypt with the server public key
    session_key = generateSessionKey()
    server_public_key = importPublicKey(res.get("server_public_key").encode('utf-8'))
    encrypted_session_key = RSAEncryption.encrypt(session_key, server_public_key)

    # call the send_session_key_to_server function to start connection with the socket
    res, status = send_session_key_to_server(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "encrypted_session_key": encrypted_session_key
        },
    )

    # check if the
    if status != 200:
        print("session key acceptance Incomplete!!!")
        return

    # save the session key in the client file
    file = open("./client_info/task3_session_key.txt", "w")
    file.truncate()
    file.writelines([("session_key:" + session_key + "\n")])
    file.close()

    print(res + "\n")

    return session_key


def sendProject(session_key, token):
    server_url = f'127.0.0.1:8000'

    # initiate the project info
    body = {
        "name": "project 3",
        "description": "lorem epsom.."
    }

    # generate IV to encrypt data than mac from encrypted_data
    iv = generateIv()
    encrypted_data = AESEncryption.encrypt(json.dumps(body), session_key, iv)

    # call the complete signUp function to start connection with the socket
    res, status = send_project(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "iv": iv,
            "encrypted_data": encrypted_data
        },
    )

    # decrypt the returned response
    res = json.loads(res)
    decrypted_message = AESEncryption.decrypt(res.get("encrypted_message"), session_key, res.get("iv"))

    print(decrypted_message)


def main():
    # get the token from the file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    token = lines[1].split(":")[1].strip()
    file.close()

    session_key = handshaking(token)
    sendProject(session_key, token)


if __name__ == "__main__":
    main()
