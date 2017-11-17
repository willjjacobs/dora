import numpy as np
import cv2
import sys
import os
# from pylibfreenect2 import Freenect2, SyncMultiFrameListener
# from pylibfreenect2 import FrameType, Registration, Frame
# from pylibfreenect2 import createConsoleLogger, setGlobalLogger
# from pylibfreenect2 import LoggerLevel
from core.neuralnet.utils import visualization_utils as vis_util



DEFAULT_RES = (240,135)
WEBCAM_PORT = 0
ADJUSTMENT_FRAMES = 2
DENOISING_PARAMS = [10,10,7,21]

#Class for connection to Kinect camera using pylibfreenect2
#Optionally supress output from pylibfreenect?
class Kinect(object):
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

#Class for webcam connection
class Webcam(object):
	def __init__(self,camera_port = WEBCAM_PORT):
		self.camera = cv2.VideoCapture(camera_port)
	def get_frame(self):
		for i in range(0,ADJUSTMENT_FRAMES):
			self.camera.read()
		retval, im = self.camera.read()
		return im
	def close(self):
		del(self.camera)

#Class for arbritrary camera connection
#TODO
class Camera(object):
	def __init__(self):
		pass
	def get_frame(self):
		pass
	def get_depth(self):
		pass
	def close(self):
		pass

class FileFeed(object):
	def __init__(self,file):
		self.feed = cv2.VideoCapture(file)
	def get_frame(self):
		retval, im = self.feed.read()
		return im
	def close(self):
		del(self.feed)

def adjust_resolution(image, new_res = DEFAULT_RES):
	return cv2.resize(image, new_res)

def convert_greyscale(image):
	return cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

def convert_color(image, init_pix, col_pix):
	color_image = cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
	#color_image[np.where((color_image == init_pix).all(axis=2))] = col_pix
	return color_image

def rotate_image(image, angle):
	rows,cols,extra = image.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
	new_image = cv2.warpAffine(image,M,(cols,rows))
	return new_image

#Smooths color images
def denoise_color(image):
	p = DENOISING_PARAMS
	return cv2.fastNlMeansDenoisingColored(image,None,p[0],p[1],p[2],p[3])
#Smooths greyscale images
def denoise_grey(image):
	p = DENOISING_PARAMS
	return cv2.fastNlMeansDenoising(image,None,p[0],p[1],p[2],p[3])

#uses uncanny edge detection
#thresholds calculated using mean pixel value and std deviation
def detect_edge(image):
	grey_image = convert_greyscale(image)
	mean_val = np.mean(grey_image)
	std = np.std(grey_image)
	low_thresh = mean_val-std
	high_thresh = mean_val+std
	edges = cv2.Canny(grey_image,low_thresh,high_thresh)
	return edges

#given an array of objects, overlay object onto original image
#TODO get vis_util working for box overlay
def overlay_image(image, dto, overlay_edges = True):

	# overlay edge detection
	edges = None
	if overlay_edges:
		edges = detect_edge(image)
		edges = convert_color(edges,[255,255,255],[0,0,255])
		image = cv2.addWeighted(image,.5,edges,.5,0)


	boxes = dto.boxes
	category_index = dto.category_index
	classes = dto.classes
	scores = dto.scores
	vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4)

	return image

#TODO given boxes from dto, find distance at center of box
def add_depth_information(depth,dto):
	boxes = dto.boxes

	x = (boxes[0] + boxes[1])/2
	y = (boxes[2] + boxes[3])/2


	depths = None
	return depths


