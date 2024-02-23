# Core
import json

# Dev
from university_project.Client.request_templates.requests_functions import complete_sign_up
from encryption.symmetric.key_generator import generateIv
from encryption.symmetric.AES import AESEncryption


def main():
    # read the symmetric_key & token from the client file
    file = open("./client_info/task1_info.txt", "r")
    lines = file.readlines()
    symmetric_key = lines[0].split(":")[1].strip()
    token = lines[1].split(":")[1].strip()
    file.close()

    # initiate the complete signUp info
    body = {
        "phone": "0988311840",
        "mobile": "+96393123456789",
        "address": "Syria, Damascus, ..."
    }

    # generate IV to encrypt data than mac from encrypted_data
    iv = generateIv()
    encrypted_data = AESEncryption.encrypt(json.dumps(body), symmetric_key, iv)

    # call the complete signUp function to start connection with the socket
    res, status = complete_sign_up(
        headers={"AUTHORIZATION": f"Token {token}"},
        body={
            "iv": iv,
            "encrypted_data": encrypted_data,
        },
    )

    # decrypt the returned response
    res = json.loads(res)
    decrypted_message = AESEncryption.decrypt(res.get("encrypted_message"), symmetric_key, res.get("iv"))

    print(status)
    print(decrypted_message)


if __name__ == "__main__":
    main()
