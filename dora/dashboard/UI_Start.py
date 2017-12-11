"""
DORA Dashboard main file
Author: Wills
Update drop down on visual change
add Button to Registered Image
"""
import sys
import numpy as np
import cv2
import json
from time import sleep
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QTableWidgetItem, QTabWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QGridLayout, QDialog, qApp, QTextEdit, QApplication, QWidget, QLineEdit, QPushButton,
    QMessageBox, QLabel, QFrame, QTableWidget, QTableWidgetItem, QCheckBox, QComboBox)
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSettings, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
#from PyQt5.QtCore.QString import QString
#from dashboard.util import *
from dashboard.util import *
import socket
import requests
import config
#from core import vision
#from core.neuralnet import NeuralNet
#import tensorflow as tf

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
    def display_hardware(self):
        hardwareD = QDialog()
        hardwareD.setMinimumSize(400,300)
        btnLayout = QHBoxLayout(self)
        layout = QVBoxLayout(self)
        textBox = QTextEdit()
        text = open('dora/dashboard/hardware.txt').read()
        textBox.setPlainText(text)
        textBox.setReadOnly(True)

        exitButton = QPushButton("Close", hardwareD)
        exitButton.setMaximumWidth(100)
        exitButton.clicked.connect(hardwareD.close)
        hardwareD.setWindowTitle("Rover Hardware")
        hardwareD.setWindowModality(Qt.ApplicationModal)
        layout.addWidget(textBox)
        layout.addLayout(btnLayout)
        btnLayout.addStretch(0)
        btnLayout.addWidget(exitButton)
        btnLayout.addStretch(0)
        hardwareD.setLayout(layout)
        hardwareD.exec_()
        print("Rover Hardware")

    @pyqtSlot()
    def display_about(self):
        aboutD = QDialog()
        aboutD.setMinimumSize(400,300)
        btnLayout = QHBoxLayout(self)
        layout = QVBoxLayout(self)
        textBox = QTextEdit()
        text1 = open('dora/dashboard/about.txt').read()
        textBox.setPlainText(text1)
        textBox.setReadOnly(True)

        exitButton = QPushButton("Close", aboutD)
        exitButton.setMaximumWidth(100)
        exitButton.clicked.connect(aboutD.close)
        aboutD.setWindowTitle("About")
        aboutD.setWindowModality(Qt.ApplicationModal)
        layout.addWidget(textBox)
        layout.addLayout(btnLayout)
        btnLayout.addStretch(0)
        btnLayout.addWidget(exitButton)
        btnLayout.addStretch(0)
        aboutD.setLayout(layout)
        aboutD.exec_()
        print("About")

    @pyqtSlot()
    def display_credits(self):
        creditsD = QDialog()
        creditsD.setMinimumSize(400,300)
        btnLayout = QHBoxLayout(self)
        layout = QVBoxLayout(self)
        textBox = QTextEdit()
        text2 = open('dora/dashboard/credits.txt').read()
        textBox.setPlainText(text2)
        textBox.setReadOnly(True)

        exitButton = QPushButton("Close", creditsD)
        exitButton.setMaximumWidth(100)
        exitButton.clicked.connect(creditsD.close)
        creditsD.setWindowTitle("Project Credits")
        creditsD.setWindowModality(Qt.ApplicationModal)
        layout.addWidget(textBox)
        layout.addLayout(btnLayout)
        btnLayout.addStretch(0)
        btnLayout.addWidget(exitButton)
        btnLayout.addStretch(0)
        creditsD.setLayout(layout)
        creditsD.exec_()
        print("Credits")




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
        if settings.value("Camera") == "Webcam":
            settings.setValue("Camera", "Kinect")
            self.tab_widget.cameraSelect.setCurrentIndex(1)
        settings.setValue("Window", "Depthmap")
        config_to_task(settings, task)
        print("Setting Display to " + task["Window"])

    @pyqtSlot()
    def set_dds(self):
        if settings.value("Camera") == "Webcam":
            settings.setValue("Camera", "Kinect")
            self.tab_widget.cameraSelect.setCurrentIndex(1)
        settings.setValue("Window", "DDS")
        config_to_task(settings, task)

    @pyqtSlot()
    def set_registered(self):
        if settings.value("Camera") == "Webcam":
            settings.setValue("Camera", "Kinect")
            self.tab_widget.cameraSelect.setCurrentIndex(1)
        settings.setValue("Window", "Registered")
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
        hardwareAct.triggered.connect(self.display_hardware)
        doraMenu.addAction(hardwareAct)

        aboutAct = QAction('&About', self)  #Add About to DORA
        aboutAct.triggered.connect(self.display_about)
        doraMenu.addAction(aboutAct)

        creditsAct = QAction('&Credits', self)  #Add Credits to DORA
        creditsAct.triggered.connect(self.display_credits)
        doraMenu.addAction(creditsAct)

        fileMenu = menubar.addMenu('&File')

        loadImageAct = QAction('&Load Image', self)
        loadImageAct.setStatusTip('TODO')
        fileMenu.addAction(loadImageAct)

        load_video_stream_act = QAction('&Load Video Stream', self)
        #load_video_stream_act.setShortcut('Ctrl+V')
        load_video_stream_act.setStatusTip('TODO')
        #load_video_stream_act.triggered.connect(self.load_video_stream_wrapper)
        fileMenu.addAction(load_video_stream_act)

        load_neural_net_act = QAction('&Load Neural Net', self)
        load_neural_net_act.setStatusTip('TODO')
        fileMenu.addAction(load_neural_net_act)

        save_image_act = QAction('&Save Image', self)
        save_image_act.setStatusTip('TODO')
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

        dds_act = QAction('Detect Drivable Surfaces', self)
        dds_act.triggered.connect(self.set_dds)
        windowMenu.addAction(dds_act)

        registered_act = QAction("Show Registered Image", self)
        registered_act.triggered.connect(self.set_registered)
        windowMenu.addAction(registered_act)

        self.setGeometry(960, 100, 960, 540)
        self.setWindowTitle('DORA')

        self.show()


class tabWidget(QWidget):
    def __init__(self, Window):
        super(QWidget, self).__init__(Window)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)
        self.testVar = 11
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
        self.tab_tools.hlayout = QHBoxLayout(self)
        #self.tab_tools.hlayout.addStretch(0)
        self.isolateToggle = QCheckBox("Isolate Sports Balls")
        self.isolateToggle.stateChanged.connect(self.isolate_toggle_act)
        self.toggleEdgeDetection = QCheckBox("Toggle Edge Detection")
        self.toggleEdgeDetection.stateChanged.connect(self.detect_edges_act)
        self.cameraSelect = QComboBox(self)
        self.cameraSelect.addItem("Webcam")
        self.cameraSelect.addItem("Kinect")
        self.cameraSelect.currentIndexChanged.connect(self.selectionchange)
        self.pushButton1 = QPushButton("Toggle Isolate Sports Ball")
        self.pushButton1.clicked.connect(self.isolate_toggle_act)
        self.pushButton2 = QPushButton("Toggle Edge Detection")
        self.pushButton2.clicked.connect(self.detect_edges_act)
        self.pushButton3 = QPushButton("Kinect")
        self.pushButton3.clicked.connect(self.toggle_kinect)
        self.pushButton4 = QPushButton("Webcam")
        self.pushButton4.clicked.connect(self.toggle_webcam)
        self.tab_tools.vlayout01.addWidget(self.cameraSelect)
        self.tab_tools.vlayout02.addWidget(self.isolateToggle)
        self.tab_tools.vlayout02.addWidget(self.toggleEdgeDetection)
        self.tab_tools.hlayout.addLayout(self.tab_tools.vlayout01)
        self.tab_tools.hlayout.addStretch(1)
        self.tab_tools.hlayout.addLayout(self.tab_tools.vlayout02)
        self.tab_tools.hlayout.addStretch(3)
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

    def selectionchange(self,i):
        print (self.cameraSelect.currentText() + " selected as input device.")
        if self.cameraSelect.currentText() == "Webcam":
            self.toggle_webcam()
        else:
            self.toggle_kinect()



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
    def detect_edges_act(self):
        if settings.value("overlay_edges") == "True":
            settings.setValue("overlay_edges", "False")
        else:
            settings.setValue("overlay_edges", "True")

        config_to_task(settings, task)

    @pyqtSlot()
    def toggle_kinect(self):
        settings.setValue("Camera","Kinect")
        config_to_task(settings, task)

    @pyqtSlot()
    def toggle_webcam(self):
        if settings.value("Window") == "DDS" or settings.value("Window") == "Depthmap":
            settings.setValue("Window", "RGB")
        settings.setValue("Camera","Webcam")
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
    data = None # class variable
    NUM_ROWS = 10
    NUM_COLS = 5

    def __init__(self, Window):
        super(QWidget, self).__init__(Window)
        vLabels = ["", "", "", "", "", "", "", "", "", ""]
        hLabels = ["OBJ#", "Type", "Location", "Certainty", "Distance"]
        self.layout = QVBoxLayout()

        data = QTableWidget()
        data.setRowCount(dataWidget.NUM_ROWS)
        data.setRowHeight(0,1)
        data.setColumnCount(dataWidget.NUM_COLS)

        data.setHorizontalHeaderLabels(hLabels)
        data.setVerticalHeaderLabels(vLabels)
        data.setColumnWidth(0,40)
        data.setColumnWidth(4,95)

        # initialize all cells empty
        # for x in range(dataWidget.NUM_ROWS):
        #     for y in range(dataWidget.NUM_COLS):
        #         data.setItem(x, y, QTableWidgetItem(""))

        dataWidget.data = data # actually assign to class
        self.layout.addWidget(data)
        self.setLayout(self.layout)

    def update_table(dto):
        print(dto)

        # initialize all cells empty
        for x in range(dataWidget.NUM_ROWS):
            for y in range(dataWidget.NUM_COLS):
                dataWidget.data.setItem(x, y, QTableWidgetItem(""))

        for row in range(len(dto)):
            # QTableWidgetItem name = dataWidget.data.item(row + 1, 0)
            dataWidget.data.setItem(row + 1, 0, QTableWidgetItem(dto[row][0]))
            dataWidget.data.setItem(row + 1, 1, QTableWidgetItem(dto[row][1]))

        # dataWidget.data.update()


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
                r_dto = requests.get('http://' + str(config.core_server_address) + ':' +str(config.core_server_port) + '/dto')
            except:
                sleep(5)
                continue
            dataWidget.update_table(r_dto.json())

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