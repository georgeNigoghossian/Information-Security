# Core
import json

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Dev
from encryption.symmetric.AES import AESEncryption
from encryption.symmetric.key_generator import generateIv


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_sign_up(request):
    body = json.loads(request.body.decode('utf-8'))

    # get the keys and data
    iv = body.get('iv')
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
