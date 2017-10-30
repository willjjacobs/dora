# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:59:47 2017

@author: Master
"""
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from dashboard.jsonsocket import *

    #runs first time program is started, sets up config file
    #Currently set up to always treat as first time
def setup_config():
    config = QSettings("CS-506", "DORA")

    config.setValue("first_setup", 1)
    first_setup = config.value("first_setup")
    if (first_setup.__eq__(0)):
        print("Not First Time Setup")
        return config
    config.setValue("first_setup", 1)
    config.setValue("test_value2", 2)
    print("First Time Setup Complete")
    return config

    #Create single constant task object, this will be updated
    #off config and sent to Core on request
def create_task():
    task = {} #Create task object

    task["first_setup"] = 0
    task["test_value2"] = 0
    task["core_ip"] = "0.0.0.0"

    return task

    #Testing Method
def print_task(task):
    print(task["first_setup"])
    print(task["test_value2"])
    print(task["core_ip"])

    #updates task object with config file data
def config_to_task(config, task):
    task["first_setup"] = config.value("first_setup")
    task["test_value2"] = config.value("test_value2")
    task["core_ip"] = config.value("core_ip")

    #Runs on program open
def open_event(config):
    #settings.setValue('testValue', 17)
    open_value = config.value("openValue")
    print('open_value = ' + str(open_value))

    #runs on program close
def close_event(config):
    config.setValue('openValue', 22)
    open_value = config.value("openValue")
    print('open_value = ' + str(open_value))

def send_task(host, port):
    server = Server(host, port)
    server.accept()
    data = server.recv()
    server.send({'data': data}).close()
    pass

#-------------------------------------
#For file menu button action methods

def load_video_stream():
    print("Connecting to Video Stream")