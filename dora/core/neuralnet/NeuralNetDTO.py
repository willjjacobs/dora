import numpy as np


class NeuralNetDTO:
    def __init__(self, boxes, category_index, classes, scores):
        self.boxes = boxes
        self.category_index = category_index
        self.classes = classes
        self.scores = scores
        self.depths = []

    def as_list(self, isolate_sports_ball, min_thresh=.15):
        result = []
        if isolate_sports_ball:
            sports_ball_index = 37
            i = np.where(self.classes == sports_ball_index)
            i = i[1].tolist()
            self.boxes = np.squeeze(self.boxes)[i]
            self.scores = np.squeeze(self.scores)[i]
            self.classes = np.squeeze(self.classes)[i]
        else:
            self.boxes = np.squeeze(self.boxes)
            self.scores = np.squeeze(self.scores)
            self.classes = np.squeeze(self.classes)

        for i in np.where(self.scores > min_thresh)[0]:
            box = self.boxes[i]
            class_name = self.category_index[self.classes[i]]["name"]
            x = int((box[0] + box[1])/2.0)
            y = int((box[2] + box[3])/2.0)
            depth = 0
            result.append([class_name, str(self.scores[i]), str(np.around(box,3)), str(depth)])
        return result