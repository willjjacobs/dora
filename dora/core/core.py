import json
from core.neuralnet import NeuralNet # as nn
from core.vision import vision
import time
import tensorflow as tf
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import socket
import cv2
import numpy as np
import sys
#from core.neuralNet import neuralNet
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

    def __init__(self):

        print("here")
        #address and port
        host = "localhost"
        port = 8000

        #start webcam
        cap = vision.Webcam()

        #from NeuralNet import NeuralNet
        nn = NeuralNet.NeuralNet('dora/core/NeuralNet/ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', 'dora/core/NeuralNet/data/mscoco_label_map.pbtxt')

        print("finished init nn");
        sys.stdout.flush();

        while True:
            #Setup socket and wait for connection
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((host, port))
            s.listen(1)
            conn,addr =s.accept()
            #sending loop
            while True:

                #get frame and overlay
                frame = cap.get_frame()
                dto = nn.run_inference(frame)
                overlayed_image = vision.overlay_image(frame,dto,False)

                #Conver image to string of uint8
                res, img_str = cv2.imencode('.jpg', overlayed_image)
                data = np.array(img_str);
                final_str = data.tostring();


                #get len of image string
                sen_len = str(len(final_str)).ljust(16);

                print("about to start sending");
                print(len(final_str));
                sys.stdout.flush();
                #finally send it
                #try and except block is for when connection cuts
                try:
                    conn.send(sen_len.encode('utf-8'));
                    conn.send(final_str);
                except ConnectionResetError:
                    break;
                # conn.close()
                time.sleep(0.5)

    """handles tasks, which then return to this function when they are over"""
    def main(self):
        while True:
            task = self.dashes["default"].get_task()
            while task != None:
                """parse command line arguments into parameters"""
                """if task is a single input command """
                if task["type"] in {"check", "distance", "number", "pixel"}:
                    self.single(task)
                    self.task = None
                else:
                    task = self.log(task)

    """ provides stream of images and data to UI"""
    def log(self,timestep, functions, parameters):
        if timestep == 0:
            return None
        self.set_networks(parameters["network"])
        dash = self.get_dash(parameters["output"])
        while True:
            task = dash.get_task()
            if task != None:
                return task
            frame = self.vision[parameters["stream"]].get_frame(parameters["resolution"])
            depth_map = self.vision["kinect"].get_depth()
            data = self.infer(frame)
            overlay = self.overlay_image(data, frame)
            self.process_data(data, parameters, depth_map)
            dash.push(data, overlay, self.depth, frame)
            time.sleep(timestep/1000)

    def set_networks(self,networks):
        """networks is dict from file names to lists of object types"""
        for nn_file in networks:
            for o_type in networks[nn_file]:
                if self.neurals[o_type].PATH_TO_CHECKPOINT != nn_file:
                    #TODO: The below line will take time to execute. Consinder printing a message.
                    #TODO: Also be sure to call NeuralNet.set_network if NN is already instantiated.
                    self.neurals[o_type] = nn.NeuralNet(nn_file)

    def get_dash(self,dash_ip):
        if ~ dash_ip in self.dashes:
            self.dashes[dash_ip] = Dashboard(dash_ip)
        return self.dashes[dash_ip]

    def single(self,parameters):
        dash = self.dashes["default"]
        self.set_networks(parameters["network"])
        frame = self.vision[parameters["stream"]].get_frame(parameters["resolution"])
        depth_map = self.vision["kinect"].get_depth()
        data = infer(frame, self.task["not_wildcard"])
        overlay = self.overlay_image(data, frame)
        self.process_data(data, parameters, depth_map)
        dash.push(data, overlay, self.depth, frame)
        with open(parameters["output"], "wb") as output:
            output.write(overlay)
        output.close()

    """uses iterator design pattern"""
    def infer(self,frame,not_wildcard):
        """dict of NN_objects"""
        data_dict = dict()
        """inefficient"""
        for obj in not_wildcard:
            object_inference = self.neurals[obj].run_inference(frame)
            for i in object_inference:
                if i.prediction == obj:
                    data_dict[obj] = i
        wildcard_inference = self.neurals["*"].run_inference(frame)
        for i in wildcard_inference:
            if ~ i.prediction in not_wildcard:
                data_dict[obj] = i
        return data_dict



#adjusts data based on user specifications
    def process_data(data, parameters, depth_map):
#holds classifications
        datas = {}
#object to be sent
        payload = {}
        for o in data:
            datas[o] = []
            for i in range(len(data[o])):
                if data[o].classes[i] == o:
                    datas[o].append(Classification(data[o].boxes[i], data[o].scores[i], data[o].distance[i]))
#remove all except for MULTI best objects
            datas[o].sort(key = lambda c: c.score)
            n = parameters["multi"][o]
            datas[o] = datas[o][:n]
            if parameters["check"]:
                if len(datas[o]) > 0:
                    payload[o]["check"] = True
            if parameters["number"]:
                payload[o]["number"] = len(datas[o])
            datas[o]["list"] = []
            for c in datas[o]:
                c_dict = {}
                if parameters["pixel"]:
                    #c_dict["pixel"] = (c.box.upper_left + c.box.lower_right)/2
                    c_dict["pixel"] = 0
                if parameters["distance"]:
                #TODO: use get_distance(pixel_coords, depth_map) to add distance for each pixel coordinate to payload
                    c_dict["distance"] = 0
                datas[o]["list"].append(c_dict)
        return json.dumps(payload)


    def add_depth(data, depth_map):
      """
        uses iterator design pattern
            adds depth value of center pixel (found by averaging top left and bottom right pixel) to each element of each object list in data
      """
      pass

    def overlay_image(data, frame, parameters):
      """uses iterator design pattern
            if parameters[pixel]:
                calls OpenCV to draw rectangles over image based on coordinates in data
                if parameters[distance]:
                    calls OpenCV to draw distances on top of rectangles
            returns edited frame
            """

c = Core()

