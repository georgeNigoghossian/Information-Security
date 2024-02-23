# Core
import json
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend

# Dev
from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption
from encryption.asymmetric.key_pair_generator import importPrivateKey, exportPublicKey
from university_project.Client.request_templates.requests_functions import send_csr, verify_csr, handshake_with_DC
from encryption.asymmetric.key_pair_generator import generateKeyPair
from encryption.digital_certificates.DigitalCertificate import DigitalCertificate


def handshaking(digital_certificate, token):
    server_url = f'127.0.0.1:8000'

    # handshaking with the server using the digital_certificate
    res, status = handshake_with_DC(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "digital_certificate": digital_certificate.public_bytes(serialization.Encoding.PEM).decode('utf-8')
        },
    )

    # check if the send csr success
    if status != 200:
        print(res)
        return

    res = json.loads(res)
    print("\nYou Have Access and the session key is" + res.get('session_key'))


def main():
    server_url = f'127.0.0.1:8000'

    # get the token from the file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    token = lines[1].split(":")[1].strip()
    file.close()

    # get client private key
    file = open("./client_info/task3_client_private_key.txt", "r")
    lines = file.read()
    file.close()
    client_private_key = importPrivateKey(lines.encode('utf-8'))

    # create CSR
    csr = DigitalCertificate.generateCSR("Twfek Ajeneh", client_private_key)
    csr = csr.public_bytes(serialization.Encoding.PEM).decode('utf-8')

    # send CSR to the CA
    res, status = send_csr(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "csr": csr
        },
    )

    # check if the send csr success
    if status != 200:
        print(res)
        print("CSR Request failed!!!")
        return

    # get the answer of the question from user
    res = json.loads(res)
    print(res.get('equation'))
    answer = input()

    # send answer to tha CA to verify csr
    res, status = verify_csr(
        server_url,
        headers={
            "Content-Type": "application/json",
            "AUTHORIZATION": f"Token {token}"
        },
        body={
            "answer": answer
        },
    )

    # check if the send csr success
    if status != 200:
        print(res)
        return

    # extract the digital_certificate from res
    res = json.loads(res)
    digital_certificate = load_pem_x509_certificate(data=res.get('digital_certificate').encode('utf-8'),
                                                    backend=default_backend())

    print("Digital Certificate")
    print("Subject: ", digital_certificate.subject)
    print("Issuer: ", digital_certificate.issuer)
    print("Serial Number: ", digital_certificate.serial_number)
    print("Not Valid Before: ", digital_certificate.not_valid_before)
    print("Not Valid After: ", digital_certificate.not_valid_after)
    print("Public Key: ", digital_certificate.public_key())

    # save the DC in the client file
    file = open("./client_info/task5_digital_certificate.txt", "w")
    file.truncate()
    file.writelines([res.get('digital_certificate')])
    file.close()

    handshaking(digital_certificate, token)


if __name__ == "__main__":
    main()
