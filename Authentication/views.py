# Core
import base64
import json
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from rest_framework import generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Dev
from .enc import encrypt, decrypt
from university_project.Server.confidentiality_tools import generate_server_keys
from .serializers import UserSerializer
from .models import User, ServerKeys
from encryption.symmetric.AES import AESEncryption
from encryption.symmetric.key_generator import generateIv
from encryption.asymmetric.key_pair_generator import importPrivateKey , exportPublicKey
from encryption.asymmetric.RSA import RSAEncryption

class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response("Welcome to the university home page", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_sign_up(request):
    body = json.loads(request.body.decode('utf-8'))

    # get the keys and data
    iv = body.get('iv')
    mac = body.get('mac')
    encrypted_data = body.get('encrypted_data')
    symmetric_key = request.user.symmetric_key

    # decrypt the data
    decrypted_data = AESEncryption.decrypt(encrypted_data, symmetric_key, iv)
    decrypted_data = json.loads(decrypted_data)

    request.user.mobile = decrypted_data.get('mobile')
    request.user.phone = decrypted_data.get('phone')
    request.user.address = decrypted_data.get('address')

    request.user.save()

    message = "complete sign up completed successfully"
    iv = generateIv()
    encrypted_message = AESEncryption.encrypt(message, symmetric_key, iv)

    res = {
        "iv": iv,
        "encrypted_message": encrypted_message
    }

    return Response(json.dumps(res), status=200)


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
    decrypted_session_key = RSAEncryption.decrypt(encrypted_session_key , server_private_key)
    request.user.session_key = decrypted_session_key
    request.user.save()

    # return the response with accept
    return Response("Session Key Accepted", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_projects(request):
    cipher_body = request.body.decode('utf-8')
    body = decrypt(cipher_body, request.user.session_key)
    body = json.loads(body)

    print("Project Received Successfully : ", body)
    return Response("Projects Received", status=200)
