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


# @pytest.mark.skipif(True, reason="Method is too slow")
@pytest.mark.xfail(reason="you know why")
def test_nn(neural_net):
    cap = cv2.VideoCapture(0)

    while (True):
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
        cv2.imshow('object detection', cv2.resize(image, (800, 600)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break