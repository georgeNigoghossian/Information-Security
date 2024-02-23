import json
from io import BytesIO

from university_project.Server.http_request_parser import http_request_parser


def execute_django(application, request, client_socket, host_port):

    environ = {
        'wsgi.input': client_socket.makefile('rb'),
        'REQUEST_METHOD': request.method,
        'PATH_INFO': request.url,
        'SERVER_NAME': host_port[0],
        'SERVER_PORT': host_port[1],
    }

    for key, value in request.headers.items():
        environ[f'HTTP_{key}'] = value

    if request.method == 'POST':
        if isinstance(request.body, dict):
            post_data_bytes = json.dumps(request.body).encode('utf-8')
        else:
            post_data_bytes = request.body
        post_data_io = BytesIO(post_data_bytes)
        environ['CONTENT_LENGTH'] = str(len(post_data_bytes))
        environ['CONTENT_TYPE'] = 'application/json'
        environ['wsgi.input'] = post_data_io

    status_code = None
    response_headers = []

    def start_response(status, headers):
        nonlocal status_code, response_headers
        status_code = status
        response_headers = headers

    response = application(environ, start_response)
    return status_code, response_headers, response


def serve_requests(client_socket, request_data, application, host_port):
    request = http_request_parser(request_data)

    status_code, response_headers, response = execute_django(application, request, client_socket, host_port)

    json_body = response._container[0].decode('utf-8')

    temp = [f"{t[0]}: {t[1]}" for t in response_headers]
    response_headers_str = "\r\n".join(temp)

    res = f"HTTP/1.1 {status_code}\r\n{response_headers_str}\r\n\r\n{json_body}".encode()

    client_socket.sendall(res)
