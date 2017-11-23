import pytest
import cv2 
from dora.core import vision
import dora.core.neuralnet.NeuralNet as NeuralNet
import tensorflow as tf 
import os 

test_color_image = cv2.imread("dora/tests/test_image.jpg", 1)
test_grey_image = cv2.imread("dora/tests/test_image.jpg", 0)

def test_sanity():
  assert test_color_image is not None  
  assert test_grey_image is not None 

@pytest.mark.xfail(reason = "kinect not kinected")
def test_kinect():
  kinect = vision.Kinect()
  assert kinect is not None
  assert kinect.get_frame() is not None
  assert kinect.get_depth() is not None 
  assert kinect.close() == 0

def test_webcam():
  webcam = vision.Webcam()
  assert webcam is not None
  assert webcam.get_frame() is not None
  assert webcam.close() == 0

@pytest.mark.xfail(reason = "arbritrary camera not implemented")
def test_camera():
  camera = vision.Camera()
  assert camera is not None
  assert camera.get_frame() is not None
  assert camera.get_depth() is not None 
  assert camera.close() == 0

def test_filefeed():
  filefeed = vision.FileFeed("Demo1.mp4")
  assert filefeed != None
  filefeed.get_frame() != None 
  assert filefeed.close() == 0

def test_adjust_resolution():
  assert vision.adjust_resolution(test_color_image) is not None
  assert vision.adjust_resolution(test_grey_image) is not None

def test_convert_greyscale():
  assert vision.convert_greyscale(test_color_image) is not None 

def test_convert_color():
  assert vision.convert_color(test_grey_image) is not None 

def test_rotate_image():
  assert vision.rotate_image(test_color_image, 15) is not None 

def test_denoise_color():
  assert vision.denoise_color(test_color_image) is not None

def test_detect_drivable_surfaces():
  assert vision.detect_drivable_surfaces(test_color_image) is not None 

def test_overlay_image():

  path_to_graph = os.path.join('dora','core','neuralnet','ssd_mobilenet_v1_coco_11_06_2017','frozen_inference_graph.pb')
  path_to_labels = os.path.join('dora','core','neuralnet', 'data', 'mscoco_label_map.pbtxt')
  neural_net = NeuralNet.NeuralNet(path_to_graph, path_to_labels)
  dto = neural_net.run_inference(test_color_image)
  assert vision.overlay_image(test_color_image, dto, True, True) is not None 
  assert vision.overlay_image(test_color_image, dto, False, True) is not None 
  assert vision.overlay_image(test_color_image, dto, False, False)  is not None 
  assert vision.overlay_image(test_color_image, dto, True, False) is not None 






