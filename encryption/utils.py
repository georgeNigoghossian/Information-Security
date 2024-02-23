from base64 import b64encode, b64decode


# convert string to byte64
def encode64(value):
    return b64decode(value);


# convert byte64 to string
def decode64(value):
    return b64encode(value).decode('utf-8')
