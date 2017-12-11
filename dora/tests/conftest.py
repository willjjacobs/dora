import pytest
import dora.core.neuralnet.NeuralNet as NeuralNet


@pytest.fixture(scope="module")
def neural_net():
    nn = NeuralNet.NeuralNet()
    nn.init_network()
    return nn
