import http.client

from . import url


class Call:

    def execute_request(self):
        pass

    def get_response_content(self):
        self.execute_request()
        self.response = self.conn.getresponse()
        return self.response.read().decode('utf-8'), self.response.status

    def close_connection(self):
        self.conn.close()

    def __init__(self, path, headers):
        self.url = url
        self.conn = http.client.HTTPConnection(self.url)
        self.method = ''
        self.path = path
        self.headers = headers
        self.response = None
        self.headers['Content-Type'] = 'application/json'
