import vision
import cv2
import matplotlib.pyplot as plt
import numpy as np
import test_dto
import tensorflow as tf
import sys 
import os
sys.path.append(os.path.abspath('../core/NeuralNet'))
sys.path.append(os.path.abspath('../core'))
import NeuralNet


IM_NAME = 'test.png'

# boxes = np.asarray([[50,50,100,100], [150,150,200,200]])
# category_index = {1: "test"}
# classes = np.asarray([1])
# scores = None
# new_dto = test_dto.NeuralNetDTO(boxes,category_index,classes,scores)
#new_webcam = vision.FileFeed("DBoverview_xVid.avi")







cap = vision.Webcam()
nn = NeuralNet.NeuralNet('ssd_mobilenet_v1_coco_11_06_2017/frozen_inference_graph.pb', 'mscoco_label_map.pbtxt')

with nn.detection_graph.as_default():
	with tf.Session(graph=nn.detection_graph) as sess: 
		while(True):
			image = cap.get_frame() 
			denoise = vision.denoise_color(image)
			dto = nn.run_inference(denoise, sess)
			overlayed_image = vision.overlay_image(denoise,dto,True)
			cv2.imshow('object detection', cv2.resize(overlayed_image, (800,600)))
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
				break
cap.close()
	


# dims = img.shape
# img = vision.adjust_resolution(img,(int(dims[1]/2),int(dims[0]/2)))
# denoise = vision.denoise_color(img)
# overlayed_image = vision.overlay_image(denoise,new_dto,True)
# cv2.imshow("overlayed_image",overlayed_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# cap = FFmpegReader("DBoverview_xVid.avi")

# for frame in cap.nextFrame():
# 	img = frame
# 	dims = img.shape
# 	print(dims)
# 	img = vision.adjust_resolution(img,(int(dims[1]/2),int(dims[0]/2)))
# 	denoise = vision.denoise_color(img)
# 	overlayed_image = vision.overlay_image(denoise,new_dto,True)
# 	cv2.imshow("overlayed_image",overlayed_image)
# 	key = cv2.waitKey(delay = 1)
# 	if key == ord('q'):
# 		cv2.destroyAllWindows()
# 		break

# cap.close()

# while(True):
	
# 	img = cap.get_frame()
# 	dims = img.shape
# 	print(dims)
# 	img = vision.adjust_resolution(img,(int(dims[1]/2),int(dims[0]/2)))
# 	denoise = vision.denoise_color(img)
# 	overlayed_image = vision.overlay_image(denoise,new_dto,True)
# 	cv2.imshow("overlayed_image",overlayed_image)
# 	key = cv2.waitKey(delay = 1)
# 	if key == ord('q'):
# 		cv2.destroyAllWindows()
# 		break

# cap.close()

# else:
# 	print("error")
# new_connection = vision.Vision()
# color = new_connection.get_depth()
# img = color.asarray(np.float32)
# cv2.imwrite(IM_NAME,img)
# new_connection.close()


#gray_img = vision.convert_greyscale(img)
#rotated_img = vision.rotate_image(img,90)
#cv2.imshow("gray_img",gray_img)
#cv2.imshow("rotated_img",rotated_img)
# cv2.imshow("img",img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# plt.figure(1)
# plt.imshow(img[:,:,0])
# plt.figure(2)
# plt.imshow(img[:,:,1])
# plt.figure(3)
# plt.imshow(img[:,:,2])
# plt.figure(4)
# plt.imshow(img[:,:,3])
# plt.show()




