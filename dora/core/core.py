import json
from core.neuralnet import NeuralNet # as nn
from core.vision import vision
import time
import tensorflow as tf
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import socket
import cv2
import socket
#from core.NeuralNet import NeuralNet
#from core.helpers import *

#dictionary which stores the tasks send by the dashboard class
task ={}

"""
Module that contains the command line app.
This is the primary entry point.
"""



class Classification:
    def __init__(self, box, score, distance):
        self.box = box
        self.score = score
        self.distance = distance

class Vision_input:
    def __init__(self, camera):
        pass

    def get_frame(self):
        pass

    def get_depth(self):
        pass




class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    """
    def do_GET(self):
        print("blaaa")
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send message back to client
        message = "Yazeed you suck!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return
    """
    def do_POST(self):
        global task;
        # Doesn't do anything with posted data
        #self._set_headers('{statusCode: 200}')
        cont_len = int(self.headers.get('content-length', 0))
        print (self.rfile.read(cont_len))



        task['multi'] = list((1, "TennisBall"),(2,"Rock"))
        task['file'] =  "filename"
        task['stream'] = "STREAM"
        task['type'] = "check"
        task ['resolution'] = [300,320]
        task['network'] = list(("filename", "rock"))
        task['output'] = "filename/STREAM"

        #
        #self.wfile.write(bytes("rtml><body><h1>POST!</h1></body></html>","utf8"))
        #self.wfile.write(bytes("fuck", "utf8"))
        #host = self.client_address.host + ":" + self.client_address.port
        self.send_response(200, "pranav")
        self.end_headers()







class Dashboard:

    def __init__(self, ip_addr):
        self.start_server()



    def start_server():
        print('starting server...')

        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = ('127.0.0.1', 8081)
        httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
        print('running server...')
        httpd.serve_forever()


    def get_task(self):
        return task



    def deref_task(self):
        global task
        task ={}


    def do_push(self,data):
        url = "http://localhost:8081"
        #r = requests.post(url,data={'number': 12524, 'type': 'issue', 'action': 'show'})
        r = requests.post(url,data)
        print(r.status_code, r.reason)
        print(r.text[:300] + '...')




class Core:
    objects = ["Tennis Ball", "Rock", "Cliff"]
    visions = dict()
    visions["webcam"] = Vision_input("webcam")
    visions["kinect"] = Vision_input("kinect")
    neurals = dict()
    dashes = dict()
    new_frame = False

    def __init__(self):
        self.cap = vision.Webcam()
        #from NeuralNet import NeuralNet
        self.nn = NeuralNet.NeuralNet('dora/core/NeuralNet/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', 'dora/core/NeuralNet/data/mscoco_label_map.pbtxt')
        #self.run()

    def get_frame(self):
        frame = self.cap.get_frame()
        dto = self.nn.run_inference(frame)
        return vision.overlay_image(frame,dto,False)
            #cv2.imshow('object detection', cv2.resize(self.overlayed_image, (800,600)))
            #if cv2.waitKey(25) & 0xFF == ord('q'):
                #cv2.destroyAllWindows()
                #break
    

