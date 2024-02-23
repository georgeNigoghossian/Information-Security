import os
import socket
import sys
import threading
import colorama
import select
from Server.HTTP import serve_requests
from university_project.wsgi import get_wsgi_application
from university_project.Server.confidentiality_tools import generate_server_keys
from Authentication.models import ServerKeys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'university_project.settings')
application = get_wsgi_application()

keep_running = True


def handle_request(client_socket, host_port):
    global keep_running

    request_data = client_socket.recv(2048)

    serve_requests(client_socket, request_data, application, host_port)

    print(colorama.Fore.RED + "closing connection" + colorama.Fore.RESET)
    client_socket.close()

    if not keep_running:
        sys.exit(0)


def server_loop(server_socket, host, port):
    global keep_running

    while keep_running:
        readable, _, _ = select.select([server_socket], [], [], 1)

        for sock in readable:
            if sock == server_socket:
                client_socket, addr = server_socket.accept()
                print(colorama.Fore.GREEN + f"Accepted connection from {addr}" + colorama.Fore.RESET)

                client_handler = threading.Thread(target=handle_request, args=(client_socket, (host, port)))
                client_handler.start()


def main():
    host = '127.0.0.1'
    port = 8000

    if not ServerKeys.objects.exists():
        generate_server_keys()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(20)
    print(f"Server listening on {host}:{port}")

    try:
        server_loop(server_socket, host, port)
    except KeyboardInterrupt:
        global keep_running
        print(colorama.Fore.YELLOW + "Shutting down..." + colorama.Fore.RESET)
        keep_running = False
        server_socket.close()


if __name__ == "__main__":
    main()
