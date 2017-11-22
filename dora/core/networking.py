from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import Request, Session
import threading
from core.core import *


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
          # parsed_path = urlparse.urlparse(self.path)
          print(self.path)
          c = self.server.get_core_instance()
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
        except Exception as e:
          print(e)
          self.send_response(400)

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
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


class dora_httpd_server(object):
    def __init__(self, server_address, port, core_instance):
        self.server = HTTPServer((server_address, port), HTTPServer_RequestHandler)
        self.thread = threading.Thread(target = self.server.serve_forever)
        self.thread.setName('DORA HTTP Server')
        self.thread.deamon = True
        self.core_instance = core_instance

    def up(self):
        self.thread.start()
        print('starting server on port {}'.format(self.server.server_port))

    def down(self):
        self.server.shutdown()
        print('stopping server on port {}'.format(self.server.server_port))

    def get_core_instance(self):
        return self.core_instance
