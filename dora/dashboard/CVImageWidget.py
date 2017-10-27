
from PyQt5.QtWidgets import (QWidget, QPushButton)
from PyQt5.QtCore import (QTimer, QPoint, pyqtSlot)
from PyQt5.QtGui import (QPainter, QColor, QImage)
import sys
import cv2
import numpy as np
import threading
import time
import queue # threadsafe

def grab(cam, queue, width, height, fps):
    capture = cv2.VideoCapture(cam)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

    while(running):
        frame = {}
        capture.grab()
        retval, img = capture.retrieve(0)
        frame["img"] = img

        if queue.qsize() < 10:
            queue.put(frame)
        else:
            print(queue.qsize())


class CVImageWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.image = None
        self.running = False
        self.q = queue.Queue()
        self.capture_thread = threading.Thread(target=grab, args = (0, self.q, 1920, 1080, 30))
        self.start_button = QPushButton("Start")

        # Timeout if we cannot update the frame
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)

        self.show()

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()

    def start_clicked(self):
        self.running = True
        self.capture_thread.start()
        self.start_button.setEnabled(False)
        self.start_button.setText('Starting...')


    def update_frame(self):
        if not self.q.empty():
            self.startButton.setText('Camera is live')
            frame = self.q.get()
            img = frame["img"]

            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation = cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QImage(img.data, width, height, bpl, QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        self.running = False



