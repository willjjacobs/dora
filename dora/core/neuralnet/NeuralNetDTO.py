class NeuralNetDTO:
    def __init__(self, boxes, category_index, classes, scores):
        self.boxes = boxes
        self.category_index = category_index
        self.classes = classes
        self.scores = scores
        self.depths = []

    def as_dict(self):
        return self.scores