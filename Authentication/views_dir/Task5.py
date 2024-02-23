# Core
import json
import random
from datetime import datetime

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from cryptography import x509

# Dev
from encryption.symmetric.key_generator import generateSessionKey
from cryptography.x509 import load_pem_x509_csr
from ..models import ServerKeys
from encryption.asymmetric.key_pair_generator import importPrivateKey
from encryption.digital_certificates.DigitalCertificate import DigitalCertificate


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_csr(request):
    # get the csr from request
    body = request.body.decode('utf-8')
    body = json.loads(body)
    csr = body.get('csr')

    # verify role
    role = request.user.role

    if role != "p":
        res = {
            "message": "unauthorized !!!"
        }

        return Response(json.dumps(res), status=401)

    # generate equation to make client solve it and give the answer
    first = random_number = random.randint(1, 10)
    second = random_number = random.randint(1, 10)

    # save the csr request in the DB
    request.user.csr_request = csr
    request.user.csr_question_answer = first + second
    request.user.save()

    # return the question to the client
    res = {
        "equation": "answer this question: " + str(first) + " + " + str(second) + " =  ?"
    }

    return Response(json.dumps(res), status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_csr(request):
    # get the csr from request
    body = request.body.decode('utf-8')
    body = json.loads(body)
    answer = body.get('answer')

    # verify role
    role = request.user.role

    if role != "p":
        res = {
            "message": "unauthorized !!!"
        }

        return Response(json.dumps(res), status=401)

    # get the csr from DB
    csr_pem = request.user.csr_request
    csr = load_pem_x509_csr(data=csr_pem.encode('utf-8'), backend=default_backend())

    # verify the csr
    isVerified = True
    if answer != request.user.csr_question_answer:
        isVerified = False

    isVerified &= DigitalCertificate.verifyCSR(csr)

    if not isVerified:
        res = {
            "message": "Invalid CSR , Verifying Failed!!!"
        }
        return Response(json.dumps(res), status=401)

    # get the server private key
    server_private_key = ServerKeys.objects.first().server_private_key
    server_private_key = importPrivateKey(server_private_key.encode('utf-8'))

    # generate Digital Certificate
    digital_certificate = DigitalCertificate.generateDigitalCertificate(csr, server_private_key)

    # return the question to the client
    res = {
        "digital_certificate": digital_certificate.public_bytes(serialization.Encoding.PEM).decode('utf-8')
    }

    return Response(json.dumps(res), status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handshake_with_dc(request):
    # get the digital_certificate from request
    body = request.body.decode('utf-8')
    body = json.loads(body)
    digital_certificate = body.get('digital_certificate')

    # verify role
    role = request.user.role

    if role != "p":
        res = {
            "message": "unauthorized !!!"
        }

        return Response(json.dumps(res), status=401)

    digital_certificate = load_pem_x509_certificate(data=digital_certificate.encode('utf-8'),
                                                    backend=default_backend())

    # verify the digital_certificate
    server_private_key = ServerKeys.objects.first().server_private_key
    server_private_key = importPrivateKey(server_private_key.encode('utf-8'))
    server_public_key = server_private_key.public_key()

    isVerified = True

    isVerified &= DigitalCertificate.verifyDigitalCertificate(digital_certificate, server_public_key)

    isVerified &= request.user.name == digital_certificate.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)[
        0].value

    isVerified &= datetime.utcnow() < digital_certificate.not_valid_after

    if not isVerified:
        res = {
            "message": "Invalid Digital Certificate"
        }
        return Response(json.dumps(res), status=400)

    # return the session to the client
    res = {
        "session_key": generateSessionKey()
    }

    return Response(json.dumps(res), status=200)
