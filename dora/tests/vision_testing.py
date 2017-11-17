from vision import vision
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from NeuralNet import NeuralNet

IM_NAME = 'test.png'

cap = vision.Webcam()
nn = NeuralNet.NeuralNet('ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', 'data/mscoco_label_map.pbtxt')

with nn.detection_graph.as_default():
	with tf.Session(graph=nn.detection_graph) as sess: 
		while(True):
			image = cap.get_frame() 
			denoise = vision.denoise_color(image)
			dto = nn.run_inference(image, sess)
			overlayed_image = vision.overlay_image(denoise,dto,True)
			cv2.imshow('object detection', cv2.resize(overlayed_image, (800,600)))
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break
cap.close()




