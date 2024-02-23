# Core
import json

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Dev
from ..models import Marks
from encryption.symmetric.AES import AESEncryption
from encryption.symmetric.key_generator import generateIv
from encryption.asymmetric.key_pair_generator import importPublicKey
from encryption.digital_signature.DigitalSignature import DigitalSignature


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_marks(request):
    body = json.loads(request.body.decode('utf-8'))

    # get the iv and data from request
    iv = body.get('iv')
    encrypted_data = body.get('encrypted_data')
    digital_signature = body.get('digital_signature')

    # get the session key and client public key from DB
    session_key = request.user.session_key
    client_pubic_key = request.user.client_public_key
    client_pubic_key = importPublicKey(client_pubic_key.encode('utf-8'))

    # verify role
    role = request.user.role

    if role != "p":
        message = "unauthorized !!!"
        iv = generateIv()
        encrypted_message = AESEncryption.encrypt(message, session_key, iv)

        res = {
            "iv": iv,
            "encrypted_message": encrypted_message
        }

        return Response(json.dumps(res), status=401)

    # verify digital signature
    verify_signature = DigitalSignature.verifyDigitalSignature(digital_signature, encrypted_data, client_pubic_key)

    if not verify_signature:
        message = "Wrong Digital Signature !!!"
        iv = generateIv()
        encrypted_message = AESEncryption.encrypt(message, session_key, iv)

        res = {
            "iv": iv,
            "encrypted_message": encrypted_message
        }

        return Response(json.dumps(res), status=401)

    # decrypt the data
    decrypted_data = AESEncryption.decrypt(encrypted_data, session_key, iv)
    decrypted_data = json.loads(decrypted_data)

    print("Marks Received Successfully : ", decrypted_data)

    # save the data for Non-Repudiation
    marks = Marks.objects.create(
        user_id=request.user.id,
        mark_list=decrypted_data,
        digital_signature=digital_signature,
        encrypted_mark_list=encrypted_data
    )
    marks.save()

    # encrypt the message
    message = "send marks completed successfully"

    iv = generateIv()
    encrypted_message = AESEncryption.encrypt(message, session_key, iv)

    res = {
        "iv": iv,
        "encrypted_message": encrypted_message
    }

    return Response(json.dumps(res), status=200)
