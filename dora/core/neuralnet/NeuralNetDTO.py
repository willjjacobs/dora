class NeuralNetDTO:
    def __init__(self, boxes, category_index, classes, scores):
        self.boxes = boxes
        self.category_index = category_index
        self.classes = classes
        self.scores = scores
        self.depths = None

    def as_dict(self):
      result = dict()
      for field in [ self.boxes, self.category_index, self.classes, self.scores, self.depths ]:
          result[field] = self.field

      return result