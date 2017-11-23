import pytest
import time
from dora.core import vision
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from core.neuralnet import NeuralNet
from core.core import Core
import _thread
import subprocess


@pytest.fixture(scope="module")
def core():
    return Core()

def test_core_instatantiate_success(core):
    assert core is not None

def test_get_latest_image(core):
    assert core.get_latest_image() is not None
