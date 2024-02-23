# Core
import json
import http.client

# Dev
from university_project.Client.API.POST import POST
from university_project.Client.API.GET import (GET)


def complete_sign_up(headers, body):
    # start connection with the socket
    req = POST("/university/api/complete_sign_up/", headers, json.dumps(body))

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status


def home(headers):
    # start connection with the socket
    req = GET("/university/api/home/", headers)

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status


def login(body):
    # start connection with the socket
    req = POST("/university/api/login/", {}, json.dumps(body))

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status


def sign_up(body):
    # start connection with the socket
    req = POST("/university/api/sign-up/", {}, json.dumps(body))

    # get the returned data
    response, status = req.get_response_content()
    response = json.loads(response)

    # close connection and return the response
    req.close_connection()
    return response, status


def key_exchange(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/key_exchange/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def send_session_key_to_server(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/send_session_key_to_server/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def send_project(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/send_projects/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def send_marks(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/send_marks/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def send_csr(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/send_csr/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def verify_csr(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/verify_csr/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status


def handshake_with_DC(url, headers, body):
    # start connection with the socket
    conn = http.client.HTTPConnection(url)
    conn.request(
        "POST",
        "/university/api/handshake_with_dc/",
        body=json.dumps(body),
        headers=headers
    )

    # get the returned data
    response = conn.getresponse()
    response_body = response.read().decode('utf-8')
    response_body = json.loads(response_body)

    # close connection and return the response
    conn.close()
    return response_body, response.status
