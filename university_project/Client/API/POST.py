import json

from university_project.Client.API.Call import Call


class POST(Call):
    def execute_request(self):
        self.conn.request(self.method, self.path, headers=self.headers, body=self.body)

    def __init__(self, path, headers, body):
        super().__init__(path, headers)
        self.method = 'POST'
        self.body = body.encode()
