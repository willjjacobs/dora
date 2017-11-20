from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import Request, Session
from threading import Thread
from core.core import *


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # parsed_path = urlparse.urlparse(self.path)
        from core.core import get_core_instance
        print(self.path)

        c = get_core_instance()
        headers = {'Content-Type': 'image/jpeg'}
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()

        # Write content as utf-8 data
        # self.wfile.write(bytes(c.get_latest_image().tostring(), "utf8"))
        self.wfile.write(c.get_latest_image().tostring())
        return

    def do_POST(self):
        global task
        # Doesn't do anything with posted data
        #self._set_headers('{statusCode: 200}')
        cont_len = int(self.headers.get('content-length', 0))
        print(self.rfile.read(cont_len))

        task['multi'] = list((1, "TennisBall"), (2, "Rock"))
        task['file'] = "filename"
        task['stream'] = "STREAM"
        task['type'] = "check"
        task['resolution'] = [300, 320]
        task['network'] = list(("filename", "rock"))
        task['output'] = "filename/STREAM"

        #
        #self.wfile.write(bytes("rtml><body><h1>POST!</h1></body></html>","utf8"))
        #self.wfile.write(bytes("fuck", "utf8"))
        #host = self.client_address.host + ":" + self.client_address.port
        self.send_response(200, "pranav")
        self.end_headers()


class Server(Thread):
    def __init__(self, ip_addr='localhost', port=8080):
        Thread.__init__(self)
        self.ip_addr = ip_addr
        self.port = port

    def run(self):
        self.start_server()

    def start_server(self):
        print('starting server...')
        # Server settings
        server_address = (self.ip_addr, self.port)
        httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
        print('running server... use <Ctrl-C> to stop')
        # try:
        httpd.serve_forever()
        # except KeyboardInterrupt:
        #     pass

    def do_push(self, data):
        url = "http://localhost:8081"
        #r = requests.post(url,data={'number': 12524, 'type': 'issue', 'action': 'show'})
        r = requests.post(url, data)
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')