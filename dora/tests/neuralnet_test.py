import pytest

import cv2
import tensorflow as tf
import sys
import os
import numpy as np
import dora.core.neuralnet.NeuralNet as NeuralNet
from dora.core.neuralnet.utils import visualization_utils as vis_util


@pytest.fixture(scope="module")
def neural_net():
    return NeuralNet.NeuralNet()


def test_neural_net_instantiate_successful(neural_net):
    assert neural_net != None
    assert neural_net.detection_graph != None
    assert neural_net.sess != None
    path_to_graph = os.path.join('dora','core','neuralnet','ssd_mobilenet_v1_coco_11_06_2017','frozen_inference_graph.pb')
    path_to_labels = os.path.join('dora','core','neuralnet', 'data', 'mscoco_label_map.pbtxt')
    neural_net = NeuralNet.NeuralNet(path_to_graph, path_to_labels)
    assert neural_net != None
    assert neural_net.detection_graph != None
    assert neural_net.sess != None


# @pytest.mark.skipif(True, reason="Method is too slow")
def test_nn_inference(neural_net):
    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_image.jpg')
    test_image = cv2.imread(img_path)
    dto = neural_net.run_inference(test_image)
    assert dto.boxes.size != 0
    assert dto.category_index.size != 0
    assert dto.classes.size != 0
    assert dto.scores.size != 0
    assert dto.depths == None

def test_set_network(neural_net):
    path_to_graph = os.path.join('dora','core','neuralnet','ssd_mobilenet_v1_coco_11_06_2017','frozen_inference_graph.pb')
    path_to_labels = os.path.join('dora','core','neuralnet', 'data', 'mscoco_label_map.pbtxt')
    neural_net.set_network(path_to_graph, path_to_labels)
    assert neural_net != None
    assert neural_net.detection_graph != None
    assert neural_net.sess != None
