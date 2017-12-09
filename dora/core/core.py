#import yaml
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

import config

global core_instance


class Core:

    def __init__(self, server_address='localhost', port=8080, dashboard_url='localhost'):
        #self.settingInit()
        # start webcam and neural net
        self.camera = vision.Webcam()
        self.kinect = None

        self.nn = NeuralNet.NeuralNet()
        self.nn.init_network()
        self.server = dora_httpd_server(server_address, port)
        self.server.up()

    def get_latest_image(self):
        #get frame and overlay

        if config.settings['Window'] =='RGB' or config.settings['Window'] =='Greyscale' :
            if config.settings['Camera'] == 'Kinect':
                print("window RGB, camera Kinect")
                frame = self.kinect.get_frame()
            elif config.settings['Camera'] == 'Webcam':
                print("window RGB, camera webcam")
                frame = self.camera.get_frame()
        elif config.settings['Window'] == 'Depthmap':
            print("window Depth Map")
            if config.settings['Camera'] == 'Kinect':
                frame = self.kinect.get_depth()





        self.dto = self.nn.run_inference(frame)

        print(config.settings['overlay_edges'])

        overlayed_image = vision.overlay_image(frame, self.dto, 
                                               overlay_edges= config.settings['overlay_edges'],
                                               isolate_sports_ball=config.settings['isolate_sports_ball'])

        if config.settings['Window'] == 'Greyscale' :
            overlayed_image = vision.convert_greyscale(overlayed_image)


        #Convert image to jpg

        retval, img_encoded = cv2.imencode('.jpg', overlayed_image)
        # TODO: check retval
        return img_encoded
    """
    def settingInit(self):
        config.settings['Camera'] = 'Webcam'
        config.settings['Window'] = 'RGB'
        config.settings['isolate_sports_ball'] = False
    """
    def settingChanger(self,stg):
        need_to_check = {'Window', 'Camera'}
        for k, v in config.settings.items():
            if stg[k] == 'True':
                stg[k] = True
            elif stg[k] == 'False':
                stg[k] = False

            if stg[k] != None and ~(k in need_to_check):
                print(k)
                config.settings[k] = stg[k]

        if stg['Camera'] == 'Kinect' and self.kinect == None:
            #TODO: return an error if no kinect
            self.kinect = vision.Kinect()

        if stg['Window'] == 'RGB':
            if stg['Camera'] == 'Kinect':
                config.settings['Window'] = 'RGB'
                config.settings['Camera'] = 'Kinect'
                return (200, "settings changed")
            elif stg['Camera'] == 'Webcam':
                config.settings['Window'] = 'RGB'
                config.settings['Camera'] = 'Webcam'
                return (200, "settings changed")
        elif stg['Window'] == 'Depthmap':
            if stg['Camera'] == 'Kinect':
                config.settings['Window'] = 'Depthmap'
                config.settings['Camera'] = 'Kinect'
                return (200, "settings changed")
            else:
                return (400, "setting not changed")
        elif stg['Window'] == 'Greyscale':
            if stg['Camera'] == 'Kinect':
                config.settings['Window'] = 'Greyscale'
                config.settings['Camera'] = 'Kinect'
                return (200, "settings changed")
            elif stg['Camera'] == 'Webcam':
                config.settings['Window'] = 'Greyscale'
                config.settings['Camera'] = 'Webcam'
                return (200, "settings changed")
        return (400, "unimplemented")

    def settingPrinter(self):
        for k, v in config.settings.items():
            print(k, v)






    def close(self):
        self.server.down()

    """
    def perform_action(self, json_data):
        print('inside perform_action' + str(json_data))
        if json_data['isolate_sports_ball'] is not None:
            if json_data['isolate_sports_ball'] == 'True':
                self.isolate_sports_ball = True
            elif json_data['isolate_sports_ball'] == 'False':
                self.isolate_sports_ball = False
    """

    def get_latest_dto(self):
        if not hasattr(self, 'dto'):
            return None
        return self.dto.as_dict()

    def main(self):
        print("in main")

def start_core():
    global core_instance
    core_instance = Core(server_address=config.core_server_address,
      port=config.core_server_port, dashboard_url=config.dashboard_address)
    return 0


def get_core_instance():
    global core_instance
    return core_instance
