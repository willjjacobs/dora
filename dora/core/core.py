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
from core.networking import HTTPServer_RequestHandler, dora_httpd_server

class Core:
    def __init__(self, server_address='localhost', port=8080, dashboard_url='localhost'):
        # start webcam and neural net
        self.cap = vision.Webcam()
        self.nn = NeuralNet.NeuralNet()
        self.server = dora_httpd_server(server_address, port, self)
        self.server.up()

    def get_latest_image(self):
        #get frame and overlay
        frame = self.cap.get_frame()
        self.dto = self.nn.run_inference(frame)
        overlayed_image = vision.overlay_image(frame, dto, False)
        #Convert image to jpg
        retval, img_encoded = cv2.imencode('.jpg', frame)
        # TODO: check retval
        return img_encoded

    def exit_gracefully(self):
        self.server.down()

    def get_latest_dto(self):
        return self.dto.as_dict()

def start_core():
    core_instance = Core()
    core_instance
    return 0

