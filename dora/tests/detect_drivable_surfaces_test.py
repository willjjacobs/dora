from dora.core import vision
import cv2
import pytest


#demo script that finds drivable surfaces
#will toss all this in a method in vision soon 
# @pytest.mark.xfail(reason = "you know why")
@pytest.mark.skipif(True, reason="Method is too slow")
def test_function():
    cap = vision.Webcam()
    image = cap.get_frame()
    dims = image.shape
    new_image = vision.adjust_resolution(image, (int(dims[1] / 2), int(
        dims[0] / 2)))
    denoise = vision.denoise_color(new_image)
    edges = vision.detect_edge(denoise)
    filled = vision.fill_edges(edges)
    eroded = vision.erode_filled(filled)
    smoothed_eroded = cv2.GaussianBlur(eroded, (15, 15), 0)
    point, new_eroded = vision.highest_point(smoothed_eroded)
    overlayed = vision.overlay_drivable_surface(new_eroded, new_image)
    cap.close()

    cv2.imshow("overlayed", overlayed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()