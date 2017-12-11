import datetime
import glob
import io
import numpy as np
import os
import pandas as pd
import core.neuralnet.train as train
import core.neuralnet.object_detection.export_inference_graph as export
from stat import S_ISREG, ST_MTIME, ST_MODE
import tensorflow as tf
import xml.etree.ElementTree as ET

import core.neuralnet.NeuralNetDTO as DTO
from core.neuralnet.utils import label_map_util
from PIL import Image
from core.neuralnet.utils import dataset_util
from collections import namedtuple, OrderedDict


class NeuralNet:

    MODEL_NAME = 'ssd_mobilenet_v1_coco_11_06_2017'
    PATH_TO_CHECKPOINT = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), MODEL_NAME,
        'frozen_inference_graph.pb')
    PATH_TO_LABELS = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'data',
        'mscoco_label_map.pbtxt')
    NUM_CLASSES = 90

    detection_graph = None

    def __init__(self, graph_path=None, label_path=None):
        # If no parameters are present, uses default Network
        if graph_path:
            self.PATH_TO_CHECKPOINT = graph_path
        if label_path:
            self.PATH_TO_LABELS = label_path

    def init_network(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CHECKPOINT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
            # Definite input and output Tensors for detection_graph
            self.image_tensor = self.detection_graph.get_tensor_by_name(
                'image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            self.detection_boxes = self.detection_graph.get_tensor_by_name(
                'detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            self.detection_scores = self.detection_graph.get_tensor_by_name(
                'detection_scores:0')
            self.detection_classes = self.detection_graph.get_tensor_by_name(
                'detection_classes:0')
            self.num_detections = self.detection_graph.get_tensor_by_name(
                'num_detections:0')
            self.sess = tf.Session(graph=self.detection_graph)
        label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(
            label_map, max_num_classes=self.NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def run_inference(self, image_np):
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image_np, axis=0)
        # Actual detection.
        (boxes, scores, classes, num) = self.sess.run(
            [
                self.detection_boxes, self.detection_scores,
                self.detection_classes, self.num_detections
            ],
            feed_dict={self.image_tensor: image_np_expanded})
        # Visualization of the results of a detection.
        '''
        '''
        dto = DTO.NeuralNetDTO(boxes, self.category_index, classes, scores)
        return dto

    def set_network(self, path_to_graph, path_to_labels):
        self.sess.close()
        self.PATH_TO_LABELS = path_to_labels
        self.PATH_TO_CHECKPOINT = path_to_graph
        self.init_network()

    def train(self, train_dir, test_dir):
        # Generate CSV
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(current_file_dir, 'data')
        training_dir = os.path.join(current_file_dir, 'training')
        config_file_path = os.path.join(data_dir, 'training.config')
        for directory in [train_dir, test_dir]:
            xml_df = self.xml_to_csv(directory)
            if (directory == train_dir):
                file = 'train'
            else:
                file = 'test'
            csv_path = os.path.join(data_dir, (file + '_label.csv'))
            xml_df.to_csv(csv_path, index=None)

            # Generate TFRecord
            record_output_path = os.path.join(data_dir, (file + '.record'))
            writer = tf.python_io.TFRecordWriter(record_output_path)
            examples = pd.read_csv(csv_path)
            grouped = split(examples, 'filename')
            for group in grouped:
                tf_example = create_tf_example(group, directory)
                writer.write(tf_example.SerializeToString())
            writer.close()

        try:
            train.train()
        except:
            print("Exporting graph file")
            # get all entries in the directory w/ stats
            entries = (os.path.join(training_dir, fn)
                       for fn in os.listdir(training_dir))
            entries = ((os.stat(path), path) for path in entries)

            # leave only regular files, insert creation date
            entries = ((stat[ST_MTIME], path) for stat, path in entries
                       if S_ISREG(stat[ST_MODE]))
            for mdate, path in sorted(entries, reverse=True):
                file_name = os.path.basename(path)
                if "model.ckpt-" in file_name:
                    checkpoint = os.path.splitext(file_name)[0]
                    break
            checkpoint_path = os.path.join(training_dir, checkpoint)
            output_path = os.path.join(training_dir, (
                'inference_graph_' + str(datetime.date.today())))
            export.export("image_tensor", config_file_path, checkpoint_path,
                          output_path)

    def xml_to_csv(self, path):
        xml_list = []
        for xml_file in glob.glob(path + '/*.xml'):
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for member in root.findall('object'):
                value = (root.find('filename').text,
                         int(root.find('size')[0].text),
                         int(root.find('size')[1].text), member[0].text,
                         int(member[4][0].text), int(member[4][1].text),
                         int(member[4][2].text), int(member[4][3].text))
                xml_list.append(value)
        column_name = [
            'filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax',
            'ymax'
        ]
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        return xml_df


    # TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'Rocks':
        return 92
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [
        data(filename, gb.get_group(x))
        for filename, x in zip(gb.groups.keys(), gb.groups)
    ]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)),
                        'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(
        feature={
            'image/height':
            dataset_util.int64_feature(height),
            'image/width':
            dataset_util.int64_feature(width),
            'image/filename':
            dataset_util.bytes_feature(filename),
            'image/source_id':
            dataset_util.bytes_feature(filename),
            'image/encoded':
            dataset_util.bytes_feature(encoded_jpg),
            'image/format':
            dataset_util.bytes_feature(image_format),
            'image/object/bbox/xmin':
            dataset_util.float_list_feature(xmins),
            'image/object/bbox/xmax':
            dataset_util.float_list_feature(xmaxs),
            'image/object/bbox/ymin':
            dataset_util.float_list_feature(ymins),
            'image/object/bbox/ymax':
            dataset_util.float_list_feature(ymaxs),
            'image/object/class/text':
            dataset_util.bytes_list_feature(classes_text),
            'image/object/class/label':
            dataset_util.int64_list_feature(classes),
        }))
    return tf_example