import json
import time
import tensorflow as tf
from http.server import BaseHTTPRequestHandler, HTTPServer
from requests import Request, Session
import socket
import cv2
import numpy as np
import sys

from core.neuralnet import NeuralNet
import core.vision as vision
from core.networking import dora_httpd_server

global core_instance


class Core:
    def __init__(self, server_address='localhost', port=8080, dashboard_url='localhost'):
        # start webcam and neural net
        self.isolate_sports_ball = False
        self.cap = vision.Webcam()
        self.nn = NeuralNet.NeuralNet()
        self.server = dora_httpd_server(server_address, port)
        self.server.up()

    def get_latest_image(self):
        #get frame and overlay
        frame = self.cap.get_frame()
        self.dto = self.nn.run_inference(frame)
        overlayed_image = vision.overlay_image(frame, self.dto, self.isolate_sports_ball)
        #Convert image to jpg
        retval, img_encoded = cv2.imencode('.jpg', overlayed_image)
        # TODO: check retval
        return img_encoded

    def close(self):
        self.server.down()

    def perform_action(json_data):
        print('inside perform_action' + json_data)
        if json_data['isolate_sports_ball'] is not None:
            if json_data['isolate_sports_ball'] == 'True':
                self.isolate_sports_ball = True
            elif json_data['isolate_sports_ball'] == 'False':
                self.isolate_sports_ball = False


    def get_latest_dto(self):
        if not hasattr(self, 'dto'):
            return None
        return self.dto.as_dict()

    def main(self):
        print("in main")

def start_core():
    global core_instance
    core_instance = Core(server_address='localhost', port=8080, dashboard_url='localhost')
    return 0


def get_core_instance():
    global core_instance
    return core_instance
