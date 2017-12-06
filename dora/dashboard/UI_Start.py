"""
DORA Dashboard main file
Author: Wills
"""
import sys
import numpy as np
import cv2
import json
from time import sleep
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QTabWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QGridLayout, QDialog, qApp, QApplication, QWidget, QLineEdit, QPushButton,
    QMessageBox, QLabel, QFrame, QTableWidget, QTableWidgetItem, QCheckBox)
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSettings, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
#from PyQt5.QtCore.QString import QString
from dashboard.util import *
#from util import *
import socket
import requests
import config
from core import vision
from core.neuralnet import NeuralNet
import tensorflow as tf

settings = setup_config()
task = create_task()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        #settings = setup_config()
        open_event(settings)
        #task = create_task()
        self.initUI()

    @pyqtSlot()
    def app_quit(self):
        print("Quitting")
        close_event(settings)
        QCoreApplication.quit()
        
    @pyqtSlot()
    def todo(self):
        print("ToDo")
        
    @pyqtSlot()
    def set_RGB(self):
        settings.setValue("Window", "RGB")
        config_to_task(settings, task)
        print("Setting Display to " + task["Window"])
        
    @pyqtSlot()
    def set_Greyscale(self):
        settings.setValue("Window", "Greyscale")
        config_to_task(settings, task)
        print("Setting Display to " + task["Window"])
        
    @pyqtSlot()
    def set_Depthmap(self):
        settings.setValue("Window", "Depthmap")
        config_to_task(settings, task)
        print("Setting Display to " + task["Window"])

    def initUI(self):
        #Create Window Widgets
        self.tab_widget = tabWidget(self)
        self.vid_widget_left = vidWidgetL(self)
        self.table_widget = dataWidget(self)

        #Create top level frame
        self.main_frame = QFrame(self)
        #self.main_frame.setStyleSheet('background-color: rgba(255, 255, 255, 1);')

        mf_layout = QGridLayout()
        mf_layout.setColumnStretch(0, 4)
        mf_layout.setColumnStretch(1, 4)

        mf_layout.addWidget(self.tab_widget, 2, 0, 4, 4)
        mf_layout.addWidget(self.vid_widget_left, 0, 1, 2, 2)
        mf_layout.addWidget(self.table_widget, 0, 0, 1, 1)

        self.main_frame.setLayout(mf_layout)

        self.setCentralWidget(self.main_frame)

        menubar = self.menuBar()  #Create Menu Bar
        doraMenu = menubar.addMenu('&DORA')  #Create DORA Menu

        hardwareAct = QAction('&Hardware', self)  #Add Hardware to DORA
        doraMenu.addAction(hardwareAct)

        aboutAct = QAction('&About', self)  #Add About to DORA
        doraMenu.addAction(aboutAct)

        creditsAct = QAction('&Credits', self)  #Add Credits to DORA
        doraMenu.addAction(creditsAct)

        fileMenu = menubar.addMenu('&File')

        loadHardwareProfileAct = QAction('&Load Hardware Profile', self)
        fileMenu.addAction(loadHardwareProfileAct)

        loadImageAct = QAction('&Load Image', self)
        fileMenu.addAction(loadImageAct)

        load_video_stream_act = QAction('&Load Video Stream', self)
        #load_video_stream_act.setShortcut('Ctrl+V')
        #load_video_stream_act.setStatusTip('Connects to video stream for display')
        #load_video_stream_act.triggered.connect(self.load_video_stream_wrapper)
        fileMenu.addAction(load_video_stream_act)

        load_neural_net_act = QAction('&Load Neural Net', self)
        fileMenu.addAction(load_neural_net_act)

        save_image_act = QAction('&Save Image', self)
        fileMenu.addAction(save_image_act)

        exitAct = QAction('&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.app_quit)
        fileMenu.addAction(exitAct)

        #Create Window Menu
        windowMenu = menubar.addMenu('&Window')

        RGB_visual_act = QAction('&RGB', self)
        RGB_visual_act.setStatusTip('Set Display Window to RGB')
        RGB_visual_act.triggered.connect(self.set_RGB)
        windowMenu.addAction(RGB_visual_act)

        greyscale_visual_act = QAction('Greyscale', self)
        greyscale_visual_act.setStatusTip('Set Display Window to Grayscale')
        greyscale_visual_act.triggered.connect(self.set_Greyscale)
        windowMenu.addAction(greyscale_visual_act)

        depthmap_visual_act = QAction('Depth Map', self)
        depthmap_visual_act.setStatusTip('Set Display Window to Depthmap')
        depthmap_visual_act.triggered.connect(self.set_Depthmap)
        windowMenu.addAction(depthmap_visual_act)

        datatable_act = QAction('Data Table', self)
        datatable_act.triggered.connect(self.todo)
        windowMenu.addAction(datatable_act)

        #Create Settings Menu
        settingsMenu = menubar.addMenu('&Settings')

        preferences_act = QAction('&Preferences', self)
        preferences_act.triggered.connect(self.todo)
        settingsMenu.addAction(preferences_act)

        preprocessing_act = QAction('&Pre-Processing', self)
        preprocessing_act.triggered.connect(self.todo)
        settingsMenu.addAction(preprocessing_act)

        self.setGeometry(960, 100, 960, 540)
        self.setWindowTitle('DORA')

        self.show()


class tabWidget(QWidget):
    def __init__(self, Window):
        super(QWidget, self).__init__(Window)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_tools = QWidget()
        self.tab_console = QWidget()
        self.tab_log = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab_tools, "Tools")
        self.tabs.addTab(self.tab_console, "Console")
        self.tabs.addTab(self.tab_log, "Log")

        # Create Tools tab
        self.tab_tools.vlayout01 = QVBoxLayout(self)
        self.tab_tools.vlayout02 = QVBoxLayout(self)
        self.tab_tools.vlayout01.addStretch(1)
        self.tab_tools.vlayout02.addStretch(1)
        self.tab_tools.hlayout = QHBoxLayout(self)
        self.tab_tools.hlayout.addStretch(0)

        self.b1 = QCheckBox("Checkbox 1")
        self.pushButton1 = QPushButton("Toggle Isolate Sports Ball")
        self.pushButton1.clicked.connect(self.isolate_toggle_act)
        self.pushButton2 = QPushButton("DevTool 02")
        self.pushButton2.clicked.connect(self.detect_edges_act)
        self.pushButton3 = QPushButton("DevTool 03")
        self.pushButton4 = QPushButton("DevTool 04")
        self.tab_tools.vlayout01.addWidget(self.pushButton1)
        self.tab_tools.vlayout01.addWidget(self.pushButton2)
        self.tab_tools.vlayout02.addWidget(self.pushButton3)
        self.tab_tools.vlayout02.addWidget(self.pushButton4)
        self.tab_tools.hlayout.addWidget(self.b1)
        self.tab_tools.hlayout.addLayout(self.tab_tools.vlayout01)
        self.tab_tools.hlayout.addLayout(self.tab_tools.vlayout02)
        self.tab_tools.setLayout(self.tab_tools.hlayout)

        # Create Console tab
        #Setup Layout
        self.tab_console.layout = QVBoxLayout(self)
        self.tab_console.layout.addStretch(1)
        #self.console_input.move(0,0)
        self.tab_console.setLayout(self.tab_console.layout)

        #Console Input fiel
        self.console_input = QLineEdit(self)
        self.console_input.returnPressed.connect(self.on_command)

        #Add widgets to tab
        self.tab_console.layout.addWidget(self.console_input)

        # Create logs tab
        # TODO

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def isolate_toggle_act(self):
        if settings.value("isolate_toggle") == "True":
            settings.setValue("isolate_toggle", "False")
        else:
            settings.setValue("isolate_toggle", "True")

        #print(settings.value("isolate_toggle"))
        #print (task["isolate_toggle"])
        config_to_task(settings, task)
        #print (task["isolate_toggle"])
        
    @pyqtSlot()
    def detect_edge_act(self):
        if settings.value("overlay_edges") == "True":
            settings.setValue("overlay_edges", "False")
        else:
            settings.setValue("overlay_edges", "True")
            
        config_to_task(settings, task)


    @pyqtSlot()
    def on_command(self):
        console_input = self.console_input.text()
        self.console_input.setText("")
        if console_input.__eq__("print task"):
            #print_task(Window.task)
            print(console_input)
        if console_input.__eq__("console to task"):
            #config_to_task(config, task)
            print(console_input)


class dataWidget(QWidget):
    def __init__(self, Window):
        super(QWidget, self).__init__(Window)
        self.layout = QVBoxLayout()

        self.data = QTableWidget()
        self.data.setRowCount(7)
        self.data.setColumnCount(5)

        self.layout.addWidget(self.data)
        self.setLayout(self.layout)


class vidWidgetL(QWidget):
    def __init__(self, Window):
        super(QWidget, self).__init__(Window)
        left_video = QLabel(self)
        left_video.move(20, 20)
        left_video.resize(400, 300)
        th = Thread(self)
        th.changePixmap.connect(lambda p: left_video.setPixmap(p))
        th.start()


class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

    def run(self):
        while True:
            try:
                r = requests.get('http://' + str(config.core_server_address) + ':' +str(config.core_server_port) + '/video_feed')
            except:
                sleep(5)
                continue
            nparr = np.fromstring(r.content, dtype=np.uint8)
            try:
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            except:
                continue
            #find params and correct color channels
            height, width, channel = image.shape
            bytesPerLine = channel * width
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB, image)

            #convert to pyQt image
            rgbImage = QImage(image, width, height, bytesPerLine,
                              QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(rgbImage)
            p = convertToQtFormat.scaled(400, 300, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)


def ui_main():
    global app  # make available elsewhere - only need to declare global if we assign
    app = QApplication(sys.argv)
    window = Window()
    app.aboutToQuit.connect(app.deleteLater)
    return app.exec_()


if __name__ == '__main__':
    ui_main()