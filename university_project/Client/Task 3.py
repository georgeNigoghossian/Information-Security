import base64
import http.client
import json
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from university_project.Client.confidentiality_tools import generate_client_keys
from university_project.Client.login import login


def achieve_confidentiality():
    host, port = '127.0.0.1', 8000
    host_port = f'{host}:{port}'

    token = login(host_port, {"username": "admin7", "password": "12345678"})
    if token is None:
        print('Login failed')
        return

    conn = http.client.HTTPConnection(host_port)

    public_key = generate_client_keys()

    body={
        "public_key":public_key.decode('utf-8')
    }
    body = json.dumps(body)

    headers = {"Content-Type": "application/json", "AUTHORIZATION": f"Token {token}"}
    conn.request("POST", "/university/api/key_exchange/", body=body.encode(),headers=headers)

    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    server_public_key = RSA.import_key(response_body["server_public_key"])
    session_key = os.urandom(32)
    cipher = PKCS1_OAEP.new(server_public_key)
    encrypted_session_key = cipher.encrypt(session_key)



    body={
        "encrypted_session_key":base64.b64encode(encrypted_session_key).decode('utf-8')
    }
    body = json.dumps(body)

    conn.request("POST", "/university/api/send_session_key/", body=body.encode(), headers=headers)

    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    if response.status == 200:
        conn.close()
        print("Response Body:", response_body)
        return response_body
    else:
        return None


def main():
    achieve_confidentiality()


if __name__ == "__main__":
    main()
