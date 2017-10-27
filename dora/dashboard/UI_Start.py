#!/usr/bin/python3
# -*- coding: utf-8 -*-
#Test
"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""
from .util import *
import cv2
import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, QTabWidget,
                             QVBoxLayout, QHBoxLayout, qApp, QApplication,
                             QWidget, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import QCoreApplication, pyqtSlot, QSettings
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtGui import QFont


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.settings = QSettings("CS-506", "DORA")
        open_event(self.settings)

        self.initUI()

    @pyqtSlot()
    def app_quit(self):
        print("Quitting")
        close_event(self.settings)
        QCoreApplication.quit()


    def initUI(self):
        #Create tabs
        self.table_widget = tabWidget(self)
        self.setCentralWidget(self.table_widget)

        menubar = self.menuBar() #Create Menu Bar
        doraMenu = menubar.addMenu('&DORA') #Create DORA Menu

        hardwareAct = QAction('&Hardware', self) #Add Hardware to DORA
        doraMenu.addAction(hardwareAct)

        aboutAct = QAction('&About', self) #Add About to DORA
        doraMenu.addAction(aboutAct)

        creditsAct = QAction('&Credits', self) #Add Credits to DORA
        doraMenu.addAction(creditsAct)

        #Create File Menu
        fileMenu = menubar.addMenu('&File')

        loadHardwareProfileAct = QAction('&Load Hardware Profile', self)
        fileMenu.addAction(loadHardwareProfileAct)

        loadImageAct = QAction('&Load Image', self)
        fileMenu.addAction(loadImageAct)

        load_video_stream_act = QAction('&Load Video Stream', self)
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
        windowMenu.addAction(RGB_visual_act)

        greyscale_visual_act = QAction('Greyscale', self)
        windowMenu.addAction(greyscale_visual_act)

        depthmap_visual_act = QAction('Depth Map', self)
        windowMenu.addAction(depthmap_visual_act)

        datatable_act = QAction('Data Table', self)
        windowMenu.addAction(datatable_act)

        #Create Settings Menu
        settingsMenu = menubar.addMenu('&Settings')

        preferences_act = QAction('&Preferences', self)
        settingsMenu.addAction(preferences_act)

        preprocessing_act = QAction('&Pre=Processing', self)
        settingsMenu.addAction(preprocessing_act)

        self.setGeometry(960,100,960,540)
        self.setWindowTitle('ICON')
        #self.setWindowIcon(QIcon('web.png'))

        self.show()

class tabWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addStretch(1)

          # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab_tools = QWidget()
        self.tab_console = QWidget()
        self.tab_log = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab_tools,"Tools")
        self.tabs.addTab(self.tab_console,"Console")
        self.tabs.addTab(self.tab_log,"Log")

        # Create Tools tab
        self.tab_tools.vlayout01 = QVBoxLayout(self)
        self.tab_tools.vlayout02 = QVBoxLayout(self)
        self.tab_tools.vlayout01.addStretch(1)
        self.tab_tools.vlayout02.addStretch(1)
        self.tab_tools.hlayout = QHBoxLayout(self)
        self.tab_tools.hlayout.addStretch(0)
        self.pushButton1 = QPushButton("DevTool 01")
        self.pushButton2 = QPushButton("DevTool 02")
        self.pushButton3 = QPushButton("DevTool 03")
        self.pushButton4 = QPushButton("DevTool 04")
        self.tab_tools.vlayout01.addWidget(self.pushButton1)
        self.tab_tools.vlayout01.addWidget(self.pushButton2)
        self.tab_tools.vlayout02.addWidget(self.pushButton3)
        self.tab_tools.vlayout02.addWidget(self.pushButton4)
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
    def on_command(self):
        print("\n")
        print(self.console_input.text())
        self.console_input.setText("")

    @pyqtSlot()
    def on_click(self):
        print("\n")

def ui_main():
  global app # make available elsewhere - only need to declare global if we assign
  app = QApplication(sys.argv)
  window = Window()
  app.aboutToQuit.connect(app.deleteLater)
  sys.exit(app.exec_())

if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Window()
  app.aboutToQuit.connect(app.deleteLater)
