import pytest
import cv2
from dora.core import vision

test_color_image = cv2.imread("dora/tests/test_image.jpg", 1)
test_grey_image = cv2.imread("dora/tests/test_image.jpg", 0)
test_depth_image = cv2.imread("dora/tests/depth_for_dds.jpg", 0)


def test_webcam():
    webcam = vision.Selector("webcam")
    assert webcam is not None
    assert webcam.get_frame() is not None
    assert webcam.close() == 0


@pytest.mark.xfail(reason="kinect not kinected")
def test_kinect():
    kinect = vision.Selector("kinect")
    assert kinect is not None
    assert kinect.get_frame() is not None
    assert kinect.get_depth() is not None
    assert kinect.close() == 0


@pytest.mark.xfail(reason="arbritrary camera not implemented")
def test_camera():
    camera = vision.Selector("camera")
    assert camera is not None
    assert camera.get_frame() is not None
    assert camera.get_depth() is not None
    assert camera.close() == 0


def test_filefeed():
    filefeed = vision.Selector("filefeed", file="dora/tests/Demo1.mp4")
    assert filefeed is not None
    assert filefeed.get_frame() is not None
    assert filefeed.close() == 0


def test_adjust_resolution():
    assert vision.adjust_resolution(test_color_image) is not None
    assert vision.adjust_resolution(test_grey_image) is not None


def test_convert_greyscale():
    assert vision.convert_greyscale(test_color_image) is not None


def test_convert_color():
    assert vision.convert_color(test_grey_image) is not None


def test_denoise_color():
    assert vision.denoise_color(test_color_image) is not None


def test_detect_drivable_surfaces_color():
    assert vision.detect_drivable_surfaces_color(test_color_image) is not None


def test_depth_drivable_surfaces():
    assert vision.depth_drivable_surfaces(test_depth_image, test_depth_image,
                                          .1) is not None


@pytest.mark.xfail(reason="No depth map")
def test_add_depth_information(neural_net):
    dto = neural_net.run_inference(test_color_image)
    assert vision.add_depth_information(None, dto) is not None


def test_overlay_image(neural_net):
    dto = neural_net.run_inference(test_color_image)
    assert vision.overlay_image(test_color_image, dto, True, True) is not None
    assert vision.overlay_image(test_color_image, dto, False, True) is not None
    assert vision.overlay_image(test_color_image, dto, False,
                                False) is not None
    assert vision.overlay_image(test_color_image, dto, True, False) is not None
