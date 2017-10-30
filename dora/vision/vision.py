import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

DEFAULT_RES = (240,135)

class Vision(object):
	def __init__(self):
		try:
			from pylibfreenect2 import OpenCLPacketPipeline
			pipeline = OpenCLPacketPipeline()
		except:
			try:
				from pylibfreenect2 import OpenGLPacketPipeline
				pipeline = OpenGLPacketPipeline()
			except:
				from pylibfreenect2 import CpuPacketPipeline
				pipeline = CpuPacketPipeline()

		print("Packet pipeline:", type(pipeline).__name__)

		self.fn = Freenect2()
		self.num_devices = self.fn.enumerateDevices()
		if self.num_devices == 0:
			print("No device connected!")
			sys.exit(1)

		self.serial = self.fn.getDeviceSerialNumber(0)
		self.device = self.fn.openDevice(self.serial, pipeline=pipeline)

		self.listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir | FrameType.Depth)
		self.device.setColorFrameListener(self.listener)
		self.device.setIrAndDepthFrameListener(self.listener)
		self.device.start()

		self.undistorted = Frame(512, 424, 4)
		self.registered = Frame(512, 424, 4)


	def get_frame(self):
		return self.listener.waitForNewFrame()["color"]

	def close(self):
		self.device.stop()
		self.device.close()

	def get_depth(self):
		return self.listener.waitForNewFrame()["depth"]

def adjust_resolution(image, new_res = DEFAULT_RES):
	return cv2.resize(image, new_res)

def convert_greyscale(image):
	return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def rotate_image(image, angle):
	rows,cols,extra = image.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
	new_image = cv2.warpAffine(image,M,(cols,rows))
	return new_image

def remove_mean(image):

	return new_image

def detect_edge(image):

	return new_image



