import json
from http.server import HTTPServer, BaseHTTPRequestHandler

USERS_LIST = [
    {
        "id": 1,
        "username": "theUser",
        "firstName": "John",
        "lastName": "James",
        "email": "john@email.com",
        "password": "12345",
    }
]


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_response(self, status_code=200, body=None):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body if body else {}).encode('utf-8'))

    def _pars_body(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        return json.loads(self.rfile.read(content_length).decode('utf-8'))  # <--- Gets the data itself

    def do_GET(self):
        if self.path == '/users':
            return self._set_response(200, USERS_LIST)
        for user in USERS_LIST:
            if self.path == f"/user/{user['username']}":
                return self._set_response(200, user)
            else:
                return self._set_response(400, {'error': 'User not found'})

    def do_POST(self):
        try:
            data = self._pars_body()
            if type(data) == dict:
                data = [data]
            id_data = []
            for d in data:
                if d['id'] in id_data or d['id'] == 1:
                    return self._set_response(400)
                else:
                    id_data.append(d['id'])
            if len(data) == 1:
                return self._set_response(201, data[0])

            return self._set_response(201, data)
        except:
            return self._set_response(400)

    def do_PUT(self):
        keywords = ['username', 'firstName', 'lastName', 'email', 'password']
        parsing = self._pars_body()

        for user in USERS_LIST:
            if keywords == list(parsing.keys()) \
                    and self.path == f"/user/{user['id']}":
                parsing.update({'id': user['id']})
                return self._set_response(200, parsing)
            elif self.path != f"/user/{user['id']}":
                return self._set_response(404, {'error': 'User not found'})
            else:
                return self._set_response(400, {'error': 'not valid request data'})

    def do_DELETE(self):
        for user in USERS_LIST:
            if self.path == f"/user/{user['id']}":
                return self._set_response(200, {})
            else:
                return self._set_response(404, {'error': 'User not found'})


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, host='localhost', port=8000):
    server_address = (host, port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
