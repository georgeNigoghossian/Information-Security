import json

from rest_framework import generics

from .enc import encrypt, decrypt
from university_project.Server.confidentiality_tools import generate_server_keys
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def home(request):
    return Response("this is university home page", status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_sign_up(request):
    cipher_body = request.body.decode('utf-8')
    body = decrypt(cipher_body, request.user.national_id)
    body = json.loads(body)

    request.user.mobile = body.get('mobile')
    request.user.phone = body.get('phone')
    request.user.address = body.get('address')

    request.user.save()

    res = json.dumps({'message': 'complete sign up completed successfully'})
    cipher_text = encrypt(res, request.user.national_id)

    return Response(cipher_text, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def key_exchange(request):
    private_key,public_key= generate_server_keys()

    request.user.private_key = private_key.decode('utf-8')
    request.user.public_key = json.loads(request.body.decode('utf-8')).get("public_key")

    request.user.save()


    # with open("server_private_key.pem", "rb") as f:
    #     private_key = RSA.import_key(f.read())
    #
    # body_contents = request.body.decode('utf-8')
    # session_key = private_key.decrypt(encrypted_session_key)


    response = {
        "server_public_key":public_key
    }
    return Response(response, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_session_key(request):

    response = {
        "server_public_key":"yes"
    }
    print(response)
    return Response(response, status=200)
