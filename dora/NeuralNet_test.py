import cv2
import tensorflow as tf
import sys
import os
import numpy as np
import core.neuralnet.NeuralNet as NeuralNet
from core.neuralnet.utils import visualization_utils as vis_util

cap = cv2.VideoCapture(0)
MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
nn = NeuralNet.NeuralNet(os.path.join('core','neuralnet',MODEL_NAME, 'frozen_inference_graph.pb'),os.path.join('core','neuralnet','data', 'mscoco_label_map.pbtxt'))


while(True):
    ret, image = cap.read()      
    dto = nn.run_inference(image)
    vis_util.visualize_boxes_and_labels_on_image_array(
        image,
        np.squeeze(dto.boxes),
        np.squeeze(dto.classes).astype(np.int32),
        np.squeeze(dto.scores),
        dto.category_index,
        use_normalized_coordinates=True,
        line_thickness=8)
    cv2.imshow('object detection', cv2.resize(image, (800,600)))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break