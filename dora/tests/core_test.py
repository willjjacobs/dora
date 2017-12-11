# import pytest
# from dora.core import vision
# from core.neuralnet import NeuralNet
# from core.core import Core


def test_core_instatantiate_success(core):
    assert core is not None


def test_get_latest_image(core):
    assert core.get_latest_image() is not None
