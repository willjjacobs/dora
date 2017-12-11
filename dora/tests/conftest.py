import pytest
import dora.core.neuralnet.NeuralNet as NeuralNet
from core.core import Core


@pytest.fixture(scope="module")
def neural_net():
    nn = NeuralNet.NeuralNet()
    nn.init_network()
    return nn


@pytest.fixture(scope="module")
def core():
    return Core()
