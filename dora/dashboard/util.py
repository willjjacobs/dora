# -*- coding: utf-8 -*-
"""
Created on Fri Oct 27 10:59:47 2017

@author: Master
"""
from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
from jsonsocket import *


def setup_config():
    config = QSettings("CS-506", "DORA")
    
    config.setValue("first_setup", 1)
    first_setup = config.value("first_setup")
    if (first_setup.__eq__(0)):
        print("Not First Time Setup")
        return config
    config.setValue("first_setup", 1)
    config.setValue("test_value2", 2)
    config.setValue("test_value3", 3)
    
    test_value1 = config.value("first_setup")
    test_value2 = config.value("test_value2")
    test_value3 = config.value("test_value3")
    print(test_value1, test_value2, test_value3)
    print("First Time Setup Complete")
    return config

def open_event(config):
    #settings.setValue('testValue', 17)
    open_value = config.value("openValue")
    print('open_value = ' + str(open_value))

    
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