import numpy as np
import os
import tensorflow as tf

from utils import label_map_util
from utils import visualization_utils as vis_util

class NeuralNet:

    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    # Assumes working directory is root of git repo
    PATH_TO_CHECKPOINT = os.path.join('dora','NeuralNet',MODEL_NAME, 'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join('dora','NeuralNet','data', 'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90

    detection_graph = None

    def __init__(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CHECKPOINT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            # Definite input and output Tensors for detection_graph
            self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def run_inference(self, image_np, sess):                       
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        # Visualization of the results of a detection.
        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=8)
        return image_np

    #def set_network(path_to_graph):
        
    #def train():
