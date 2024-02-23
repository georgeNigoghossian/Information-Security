import json

from http_parser.parser import HttpParser


def is_valid_json(string):
    try:
        return json.loads(string)
    except ValueError:
        return False


class http_request_parser:
    def __init__(self, request_string):
        parser = HttpParser()
        parser.execute(request_string, len(request_string))

        self.method = parser.get_method()
        self.url = parser.get_url()
        self.headers = parser.get_headers()
        self.body = None

        if parser.is_partial_body():
            str = parser.recv_body()

            if body := is_valid_json(str):  # if body is valid json then decode it
                self.body = body
            else:    # if it is ciphered then kepp it as is
                self.body = str
