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


class Core:
    def __init__(self, host='localhost', port=8080, dashboard_url='localhost'):
        # start webcam and neural net
        self.cap = vision.Webcam()
        # self.nn = NeuralNet.NeuralNet()
        self.server = Server(ip_addr=host, port=port)

    def get_latest_image():
        #get frame and overlay
        frame = self.cap.get_frame()
        # dto = self.nn.run_inference(frame)
        # overlayed_image = vision.overlay_image(frame, dto, False)
        #Convert image to jpg
        retval, img_encoded = cv2.imencode('.jpg', frame)
        # TODO check retval
        # img_encoded.tostring() ??
        return img_encoded

    def main(self):
        print("in main")

        # while True:

        #     response = requests.post(
        #         self.host_url, headers=headers, data=img_encoded.tostring())
        #     time.sleep(0.5)

        # print("After requests loop")
        # break


def start_core():
    global c
    c = Core()
    return 0


def get_core_instance():
    return c
