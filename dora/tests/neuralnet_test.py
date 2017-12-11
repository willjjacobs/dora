import pytest

import cv2
import os
import dora.core.neuralnet.NeuralNet as NeuralNet


@pytest.fixture(scope="module")
def neural_net():
    nn = NeuralNet.NeuralNet()
    nn.init_network()
    return nn


def test_neural_net_instantiate_successful(neural_net):
    assert neural_net is not None
    assert neural_net.detection_graph is not None
    assert neural_net.sess is not None
    path_to_graph = os.path.join('dora', 'core', 'neuralnet',
                                 'ssd_mobilenet_v1_coco_11_06_2017',
                                 'frozen_inference_graph.pb')
    path_to_labels = os.path.join('dora', 'core', 'neuralnet', 'data',
                                  'mscoco_label_map.pbtxt')
    neural_net = NeuralNet.NeuralNet(path_to_graph, path_to_labels)
    neural_net.init_network()
    assert neural_net is not None
    assert neural_net.detection_graph is not None
    assert neural_net.sess is not None


# @pytest.mark.skipif(True, reason="Method is too slow")
def test_nn_inference(neural_net):
    img_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'test_image.jpg')
    test_image = cv2.imread(img_path)
    dto = neural_net.run_inference(test_image)
    assert dto.boxes.size != 0
    assert dto.category_index is not None
    assert dto.classes.size != 0
    assert dto.scores.size != 0
    assert dto.depths == []


def test_set_network(neural_net):
    path_to_graph = os.path.join('dora', 'core', 'neuralnet',
                                 'ssd_mobilenet_v1_coco_11_06_2017',
                                 'frozen_inference_graph.pb')
    path_to_labels = os.path.join('dora', 'core', 'neuralnet', 'data',
                                  'mscoco_label_map.pbtxt')
    neural_net.set_network(path_to_graph, path_to_labels)
    assert neural_net is not None
    assert neural_net.detection_graph is not None
    assert neural_net.sess is not None
