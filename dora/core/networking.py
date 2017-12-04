from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import Request, Session
import threading
from core.core import *
# import core.core
# from core.core import get_core_instance

class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # try:
            from core.core import get_core_instance
            c = get_core_instance()

            if (self.path == '/video_feed'):
                # Send response status code
                self.send_response(200)
                # Send headers
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(c.get_latest_image().tostring())
                return
            elif (self.path == '/dto'):
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                params = c.get_latest_dto()
                # Write content as utf-8 data
                self.wfile.write(bytes(json.dumps(params), "utf8"))
                return
            # no response
            self.send_response(200)

        # except Exception as e:
            # print(e)
            # self.send_response(400)
        # return

    def do_POST(self):
        print('POST on ' + self.path)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        json_data = json.loads(post_body)
        c = get_core_instance()

        c.perform_action(json_data)

        self.send_response(200, "pranav")
        self.end_headers()

class dora_httpd_server(object):
    def __init__(self, server_address='localhost', port='8080'):
          self.server = HTTPServer((server_address, port), HTTPServer_RequestHandler)
          self.thread = threading.Thread(target = self.server.serve_forever)
          self.thread.setName('DORA HTTP Server')
          self.thread.deamon = True


    def up(self):
        self.thread.start()
        print('starting server on port {}'.format(self.server.server_port))

    def down(self):
        self.server.shutdown()
        print('stopping server on port {}'.format(self.server.server_port))
