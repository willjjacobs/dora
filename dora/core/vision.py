import numpy as np
import cv2
import sys
import os
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
from core.neuralnet.utils import visualization_utils as vis_util
from PIL import ImageFont

DEFAULT_RES = (240, 135)
WEBCAM_PORT = 0
ADJUSTMENT_FRAMES = 2
DENOISING_PARAMS = [10, 10, 7, 21]

#Optimize Drivable Surfaces
#Depth map

def Selector(args, camera_port = 0, file = ""):
    if (args == 'Kinect'):
        return Kinect()
    elif (args == 'Webcam'):
        return Webcam()
    elif (args == 'Filefeed'):
        return FileFeed(file)
    else: 
        return Camera(camera_port)

#ADD SELECTOR 
#Class for connection to Kinect camera using pylibfreenect2
#Optionally supress output from pylibfreenect?
class Kinect(object):
    def __init__(self):
        try:
            from pylibfreenect2 import OpenCLPacketPipeline
            pipeline = OpenCLPacketPipeline()
        except:
            try:
                from pylibfreenect2 import OpenGLPacketPipeline
                pipeline = OpenGLPacketPipeline()
            except:
                from pylibfreenect2 import CpuPacketPipeline
                pipeline = CpuPacketPipeline()
        print("Packet pipeline:", type(pipeline).__name__)
        self.type = "Kinect"
        self.fn = Freenect2()
        self.num_devices = self.fn.enumerateDevices()
        if self.num_devices == 0:
            print("No device connected!")
            sys.exit(1)
        self.serial = self.fn.getDeviceSerialNumber(0)
        self.device = self.fn.openDevice(self.serial, pipeline=pipeline)
        self.listener = SyncMultiFrameListener(FrameType.Color | FrameType.Ir |
                                               FrameType.Depth)
        self.device.setColorFrameListener(self.listener)
        self.device.setIrAndDepthFrameListener(self.listener)
        self.device.start()
        self.registration = Registration(self.device.getIrCameraParams(),
                            self.device.getColorCameraParams())
        self.undistorted = Frame(512, 424, 4)
        self.registered = Frame(512, 424, 4)

    def get_frame(self):
        frame = self.listener.waitForNewFrame()
        rgb = frame["color"].asarray().copy()
        rgb = cv2.cvtColor(rgb, cv2.COLOR_BGRA2BGR)
        self.listener.release(frame)
        return rgb
    def close(self):
        self.device.stop()
        #self.device.close()
        return 0
    def get_depth(self):
        frame = self.listener.waitForNewFrame()
        depth = frame["depth"].asarray().copy()
        self.listener.release(frame)
        return depth / 4500.0
    def get_registered(self):
        frame = self.listener.waitForNewFrame()
        depth = frame["depth"]
        color = frame["color"]
        new_depth = depth.asarray().copy() / 4500.0
        self.registration.apply(color, depth, self.undistorted, self.registered)
        self.listener.release(frame)
        return cv2.cvtColor(self.registered.asarray(np.uint8).copy(), cv2.COLOR_BGRA2BGR), new_depth

#Class for webcam connection
class Webcam(object):
    def __init__(self, camera_port=WEBCAM_PORT):
        self.camera = cv2.VideoCapture(camera_port)
        self.type = "Webcam"
    def get_frame(self):
        for i in range(0, ADJUSTMENT_FRAMES):
            self.camera.read()
        retval, im = self.camera.read()
        return im
    def close(self):
        del (self.camera)
        return 0

#Class for arbritrary camera connection
#TODO
class Camera(object):
    def __init__(self, camera_port):
        self.type = "Camera"
        self.camera = cv2.VideoCapture(camera_port)
    def get_frame(self):
        for i in range(0, ADJUSTMENT_FRAMES):
            self.camera.read()
        retval, im = self.camera.read()
        return im
    def close(self):
        del (self.camera)
        return 0

class FileFeed(object):
    def __init__(self, file):
        self.type = "Filefeed"
        self.feed = cv2.VideoCapture(file)
    def get_frame(self):
        retval, im = self.feed.read()
        return im
    def close(self):
        del (self.feed)
        return 0

def adjust_resolution(image, new_res=DEFAULT_RES):
    new_image = image.copy()
    return cv2.resize(new_image, new_res)

def convert_greyscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convert_color(image):
    color_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    return color_image

#Smooths color images
def denoise_color(image):
    p = DENOISING_PARAMS
    return cv2.fastNlMeansDenoisingColored(image, None, p[0], p[1], p[2], p[3])

#uses uncanny edge detection
#thresholds calculated using mean pixel value and std deviation
def detect_edge(image):
    grey_image = convert_greyscale(image)
    mean_val = np.mean(grey_image)
    std = np.std(grey_image)
    low_thresh = mean_val - std
    high_thresh = mean_val + std
    edges = cv2.Canny(grey_image, low_thresh, high_thresh)
    return edges

#fills from bottom up
def fill_edges(edges):
    dims = edges.shape
    filled = edges.copy()
    pix = 255
    for x in range(dims[1] - 1, -1, -1):
        for y in range(dims[0] - 1, -1, -1):
            if filled[y][x] == 255 and pix == 255:
                pix = 0
            else:
                filled[y][x] = pix
        pix = 255
    return filled

#horizontal erosion
def erode_filled(filled):
    dims = filled.shape
    eroded = filled.copy()
    width = 20
    for y in range(dims[0] - 1, -1, -1):
        count = 0
        for x in range(dims[1] - 1, -1, -1):
            if x < width or x > dims[1] - width:
                eroded[y][x] = 0
            elif eroded[y][x] == 255:
                count += 1
            else:
                if count < width and count > 0:
                    for i in range(0, count + 1):
                        eroded[y][x + i] = 0
                count = 0
    return eroded

#finds highest point on the drivable surface
def highest_point(eroded):
    R = 5
    largest = np.unravel_index(eroded.argmax(), eroded.shape)
    eroded = convert_color(eroded)
    for y in range(largest[0] - R, largest[0] + R):
        for x in range(largest[1] - R, largest[1] + R):
            eroded[y][x] = [0, 0, 255]
    return largest, eroded

def overlay_drivable_surface(highest_point, image):
    return cv2.addWeighted(highest_point, .5, image, .5, 0)

#Affected by color changes and texture 
def detect_drivable_surfaces_color(image):
    new_image = image.copy()
    denoise = denoise_color(new_image)
    edges = detect_edge(new_image)
    filled = fill_edges(edges)
    eroded = erode_filled(filled)
    smoothed_eroded = cv2.GaussianBlur(eroded, (15, 15), 0)
    point, new_eroded = highest_point(smoothed_eroded)
    overlayed = overlay_drivable_surface(new_eroded, new_image)
    return overlayed

#TODO
def calibrate(depth):
    calibration = 1
    new_depth = depth*calibration
    return new_depth 

def calculate_heights(depth, camera_height, fov = [70.6, 60]):
    kth0 = np.radians(30)
    hfov = fov[0]
    vfov = fov[1]
    size = depth.shape
    new_depth = calibrate(depth.copy())
    heights = np.zeros((size[0],size[1]))
    ang_per_hpix = hfov/size[0]
    ang_per_vpix = vfov/size[1]
    bottom_line = new_depth[size[0]-1,:]
    top_line = new_depth[int((size[0]-1)/2),:]
    # r0 = 0
    # count = 0
    # for i in range(0,len(bottom_line)):
    #     if bottom_line[i] > 5:
    #         count+=1
    #         r0+=bottom_line[i]
    # r0 = r0/count
    r0 = np.mean(bottom_line)
    print(r0)
    alpha0 = np.arccos(camera_height/r0)
    for i in range(0,size[0]):
        alpha = alpha0 + (np.radians(vfov) - np.radians(ang_per_vpix*(i)))
        for j in range(0,size[1]):  
            new_depth[i][j] = (camera_height - new_depth[i][j]*np.cos(alpha) - new_depth[i][j]*np.cos(kth0))
    return new_depth

def fill_edges_depth(edges, threshold = 5):
    dims = edges.shape
    threshold = edges.max()/threshold
    filled = edges.copy()
    pix = 255
    for x in range(dims[1] - 1, -1, -1):
        for y in range(dims[0] - 1, -1, -1):
            if filled[y][x] > threshold and pix == 255 and y < dims[0] - dims[0]/10: 
                pix = 0
            else:
                filled[y][x] = pix
        pix = 255
    return filled

#Optimize
def depth_drivable_surfaces(color, depth, camera_height, fov = [70.6, 60]):
    heights = calculate_heights(depth,camera_height,fov)
    heights = convert_color(heights).astype("uint8")
    heights = denoise_color(heights)
    #heights = cv2.GaussianBlur(heights, (15, 15), 0)
    heights = convert_greyscale(heights)
    gx, gy = np.gradient(heights,50)
    gtot = np.sqrt(gx**2 + gy**2)
    kernel = np.ones((5,5),np.float32)/50
    gtot = cv2.filter2D(gtot,-1,kernel)
    # #gtot = cv2.GaussianBlur(gtot,(5,5),0)
    filled = fill_edges_depth(gtot)
    filled = filled.astype("uint8")
    overlay = overlay_drivable_surface(depth.astype("uint8"),filled)
    overlay = convert_color(overlay)
    return overlay

# #given an array of objects, overlay object onto original image
# #TODO get vis_util working for box overlay
# def overlay_image(image, dto, overlay_edges=True):

#     # overlay edge detection
#     new_image = image.copy()
#     edges = None
#     if overlay_edges:
#         edges = detect_edge(image)
#         edges = convert_color(edges, [255, 255, 255], [0, 0, 255])
#         new_image = cv2.addWeighted(new_image, .5, edges, .5, 0)

#     boxes = dto.boxes
#     category_index = dto.category_index
#     classes = dto.classes
#     s = dto.scores
#     # Get indices and display *ONLY* sports balls
#     # Index derived from mscoco_label_map.pbtext
#     sports_ball_index = 37
#     i = np.where(classes == sports_ball_index)
#     i = i[1].tolist()
#     boxes = np.squeeze(boxes)[i]
#     s = np.squeeze(s)[i]

#     vis_util.visualize_boxes_and_labels_on_image_array(
#         new_image,
#         boxes,
#         np.squeeze(classes).astype(np.int32),
#         s,
#         category_index,
#         use_normalized_coordinates=True,
#         line_thickness=4)

#     return new_image



#given an array of objects, overlay object onto original image
#TODO get vis_util working for box overlay
def overlay_image(image, dto, overlay_edges=True, isolate_sports_ball=False):
    # overlay edge detection
    new_image = image.copy()
    edges = None
    if overlay_edges:
        edges = detect_edge(denoise_color(image))
        edges = convert_color(edges)
        new_image = cv2.addWeighted(new_image, .5, edges, .5, 0)

    boxes = dto.boxes
    category_index = dto.category_index
    classes = dto.classes
    scores = dto.scores

    # Get indices and display *ONLY* sports balls
    # Index derived from mscoco_label_map.pbtext
    # Change the below flag to false if you want to view all detected items and not just tennis
    # balls.
    if isolate_sports_ball:
        sports_ball_index = 37
        i = np.where(classes == sports_ball_index)
        i = i[1].tolist()
        boxes = np.squeeze(boxes)[i]
        scores = np.squeeze(scores)[i]
        classes = np.squeeze(classes)[i]
    else:
        boxes = np.squeeze(boxes)
        scores = np.squeeze(scores)
        classes = np.squeeze(classes)

    vis_util.visualize_boxes_and_labels_on_image_array(
        new_image,
        boxes,
        classes.astype(np.int32),
        scores,
        category_index,
        min_score_thresh = 0.15,
        use_normalized_coordinates=True,
        line_thickness=10)
    return new_image

#TODO given boxes from dto, find distance at center of box
def add_depth_information(depth, dto):
    boxes = dto.boxes
    for i in range(0,len(boxes)):
        box = boxes[i]
        x = int((box[0] + box[1]) / 2)
        y = int((box[2] + box[3]) / 2)
        d = depth[x][y]
        dto.depths.append(d)
