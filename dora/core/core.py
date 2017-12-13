import cv2

from core.neuralnet import NeuralNet
import core.vision as vision
from core.networking import dora_httpd_server

import config

global core_instance


class Core:
    def __init__(self,
                 server_address='localhost',
                 port=8080,
                 dashboard_url='localhost'):

        self.cap = None
        self.nn = NeuralNet.NeuralNet()
        self.nn.init_network()
        self.server = dora_httpd_server(server_address, port)
        self.server.up()

    def get_latest_image(self):
        '''get frame and overlay'''

        ret_frame = None
        print(config.settings['Window'])
        if self.cap is None:
            self.cap = vision.Selector(config.settings['Camera'])
        elif self.cap.type != config.settings['Camera']:
            self.cap.close()
            self.cap = vision.Selector(config.settings['Camera'])

        if (config.settings['Window'] == 'RGB' or config.settings['Window'] == 'Greyscale'):
            if config.settings['Camera'] == 'Kinect':
                print("window RGB, camera Kinect")
                frame = self.cap.get_frame()
                # #vision.adjust_resolution(, (212, 256))
                # new_depth = depth.copy()
                # new_depth *= (255.0/depth.max())
                # frame = vision.depth_drivable_surfaces(depth,new_depth,1)
            elif config.settings['Camera'] == 'Webcam':
                print("window RGB, camera webcam")
                frame = self.cap.get_frame()

            self.dto = self.nn.run_inference(frame)
            print(config.settings['overlay_edges'])
            ret_frame = vision.overlay_image(
                frame,
                self.dto,
                overlay_edges=config.settings['overlay_edges'],
                isolate_sports_ball=config.settings['isolate_sports_ball'],
                threshold = float(config.settings['network_thresh']))

            if config.settings['Window'] == 'Greyscale':
                ret_frame = vision.convert_greyscale(ret_frame)

        elif config.settings['Window'] == 'Depthmap':
            print("window Depth Map")
            if config.settings['Camera'] == 'Kinect':
                ret_frame = self.cap.get_depth() * 500.0
        elif config.settings['Window'] == 'DDS':
            print("window DDS")
            if config.settings['Camera'] == 'Kinect':
                depth = vision.adjust_resolution(self.cap.get_depth(), (212,
                                                                        256))
                new_depth = depth.copy()
                new_depth *= (255.0 / depth.max())
                ret_frame = vision.depth_drivable_surfaces(depth, new_depth, 1)
        elif config.settings['Window'] == 'Registered':
            print("window Registered")
            if config.settings['Camera'] == 'Kinect':
                frame, depth = self.cap.get_registered()
                self.dto = self.nn.run_inference(frame)
                ret_frame = vision.overlay_image(
                    frame,
                    self.dto,
                    overlay_edges=config.settings['overlay_edges'],
                    isolate_sports_ball=config.settings['isolate_sports_ball'],
                    threshold = float(config.settings['network_thresh']))
                #vision.add_depth_information(depth, self.dto)

            # TODO: check retval
        retval, img_encoded = cv2.imencode('.jpg', ret_frame)

        return img_encoded

    def settingChanger(self, stg):
        need_to_check = {'Window', 'Camera'}
        for k, v in config.settings.items():
            if stg[k] == 'True':
                stg[k] = True
            elif stg[k] == 'False':
                stg[k] = False
            if (stg[k] is not None) and (k not in need_to_check):
                print(k)
                config.settings[k] = stg[k]
        config.settings['Window'] = stg['Window']
        config.settings['Camera'] = stg['Camera']
        return (200, "its fine")

    def settingPrinter(self):
        for k, v in config.settings.items():
            print(k, v)

    def close(self):
        self.server.down()

    def get_latest_dto(self):
        if not hasattr(self, 'dto'):
            return None
        return self.dto.as_list(config.settings['isolate_sports_ball'], float(config.settings['network_thresh']))

    def main(self):
        print("in main")


def start_core():
    global core_instance
    core_instance = Core(
        server_address=config.core_server_address,
        port=config.core_server_port,
        dashboard_url=config.dashboard_address)
    return 0


def get_core_instance():
    global core_instance
    return core_instance
