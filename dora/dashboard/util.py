from PyQt5 import QtCore
from PyQt5.QtCore import QSettings
#from dashboard.jsonsocket import *
import requests
#from jsonsocket import *
import config as configfile

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
    config.setValue("isolate_toggle", "False")
    config.setValue("core_ip", "0.0.0.0")
    config.setValue("Camera",configfile.settings["Camera"])
    #config.setValue("Camera", "Webcam")
    #config.setValue("Camera", "Kinect")
    config.setValue("Window", configfile.settings["Window"])
    config.setValue("overlay_edges", "False")
    print("First Time Setup Complete")
    return config


    #Create single constant task object, this will be updated
    #off config and sent to Core on request
def create_task():
    task = {}  #Create task object

    # task["Camera"] = "Webcam"
    task["Camera"] = "Webcam"
    task["first_setup"] = 0
    task["isolate_toggle"] = "False"
    task["core_ip"] = "0.0.0.0"
    task["Window"] = "RGB"
    task["overlay_edges"] = "False"

    return task


    #Testing Method
def print_task(task):
    print(task["first_setup"])
    print(task["isolate_toggle"])
    print(task["core_ip"])


    #updates task object with config file data
def config_to_task(config, task):
    task["first_setup"] = config.value("first_setup")
    task["isolate_toggle"] = config.value("isolate_toggle")
    task["core_ip"] = config.value("core_ip")
    task["Camera"] = config.value("Camera")
    task["Window"] = config.value("Window")
    task["overlay_edges"] = config.value("overlay_edges")


    data_to_send = {'Camera' : task['Camera'],
                    'isolate_sports_ball' : task['isolate_toggle'],
                    'Window' : task['Window'],
                    'overlay_edges' : task['overlay_edges']}
    print(task["isolate_toggle"])
    print(task["overlay_edges"])

    requests.post('http://' + str(configfile.core_server_address) + ':' +str(configfile.core_server_port), json=data_to_send)



    #Runs on program open
def open_event(config):
    #settings.setValue('testValue', 17)
    open_value = config.value("openValue")


    #runs on program close
def close_event(config):
    config.setValue('openValue', 22)
    open_value = config.value("openValue")


# def send_task(host, port):
#     server = Server(host, port)
#     server.accept()
#     data = server.recv()
#     server.send({'data': data}).close()
#     pass


#-------------------------------------
#For file menu button action methods


def load_video_stream():
    print("Connecting to Video Stream")