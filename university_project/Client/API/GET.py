from university_project.Client.API.Call import Call


class GET(Call):
    def execute_request(self):
        self.conn.request(self.method, self.path, headers=self.headers)

    def __init__(self, path, headers):
        super().__init__(path, headers)
        self.method = 'GET'
