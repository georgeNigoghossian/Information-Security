# Core
import json

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Dev
from ..models import ServerKeys
from encryption.symmetric.AES import AESEncryption
from encryption.symmetric.key_generator import generateIv
from encryption.asymmetric.key_pair_generator import importPrivateKey, exportPublicKey
from encryption.asymmetric.RSA import RSAEncryption


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def key_exchange(request):
    # extract the client public key
    body = json.loads(request.body)

    # add the client public key to the user row in DB
    request.user.client_public_key = body.get("client_public_key")
    request.user.save()

    # get the server public key
    server_private_key = ServerKeys.objects.first().server_private_key
    server_private_key = importPrivateKey(server_private_key.encode('utf-8'))
    server_public_key = exportPublicKey(server_private_key.public_key()).decode('utf-8')

    # return the server public key
    res = {
        "server_public_key": server_public_key
    }
    return Response(json.dumps(res), status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def receive_session_key_from_client(request):
    # extract data from the body
    encrypted_session_key = json.loads(request.body.decode('utf-8')).get("encrypted_session_key")

    # get the server private key
    server_private_key = ServerKeys.objects.first().server_private_key
    server_private_key = importPrivateKey(server_private_key.encode('utf-8'))

    # decrypt the session key and save it
    decrypted_session_key = RSAEncryption.decrypt(encrypted_session_key, server_private_key)
    request.user.session_key = decrypted_session_key
    request.user.save()

    # return the response with accept
    return Response("Session Key Accepted", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_projects(request):
    body = json.loads(request.body.decode('utf-8'))

    # get the keys and data
    iv = body.get('iv')
    encrypted_data = body.get('encrypted_data')
    session_key = request.user.session_key

    # decrypt the data
    decrypted_data = AESEncryption.decrypt(encrypted_data, session_key, iv)
    decrypted_data = json.loads(decrypted_data)

    print("Project Received Successfully : ", decrypted_data)

    # encrypt the message
    message = "send project completed successfully"
    iv = generateIv()
    encrypted_message = AESEncryption.encrypt(message, session_key, iv)

    res = {
        "iv": iv,
        "encrypted_message": encrypted_message
    }

    return Response(json.dumps(res), status=200)
