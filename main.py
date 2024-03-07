from http.server import HTTPServer
from server.request_handler import RequestHandler


def run():
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Starting server...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
