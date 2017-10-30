import sys

import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QLabel


class Thread(QThread):
    changePixmap = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)

    def run(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 Video'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(1800, 1200)
        # create a label
        label = QLabel(self)
        label.move(280, 120)
        label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(lambda p: label.setPixmap(p))
        th.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())