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
from core.networking import *

global core_instance


class Core:
    def __init__(self, host='localhost', port=8080, dashboard_url='localhost'):
        # start webcam and neural net
        self.cap = vision.Webcam()
        self.nn = NeuralNet.NeuralNet()
        self.server = Server(ip_addr=host, port=port)
        self.server.setName('DORA HTTP Server')
        self.server.start()  # starts server thread

    def get_latest_image(self):
        #get frame and overlay
        frame = self.cap.get_frame()
        dto = self.nn.run_inference(frame)
        overlayed_image = vision.overlay_image(frame, dto, True)
        #Convert image to jpg
        retval, img_encoded = cv2.imencode('.jpg', overlayed_image)
        # TODO: check retval
        return img_encoded

    def close(self):
        self.server.terminate()

    def main(self):
        print("in main")

        # while True:

        #     response = requests.post(
        #         self.host_url, headers=headers, data=img_encoded.tostring())
        #     time.sleep(0.5)

        # print("After requests loop")
        # break


def start_core():
    global core_instance
    core_instance = Core()
    return 0


def get_core_instance():
    global core_instance
    return core_instance
