class NeuralNetDTO:

    boxes = None;
    category_index = None;
    classes = None;
    scores = None;
    distance = None;

    def __init__(self, boxes, category_index, 
    	classes, scores):
        self.boxes = boxes
        self.category_index = category_index
        self.classes = classes
        self.scores = scores



    def getBoxes(self):
    	return self.boxes

    def getScores(self):
    	return self.scores

    def getIndex(self):
    	return self.category_index

    def setDitance(self, dist):
    	self.distance = dist

    def getDistance(self):
    	return self.distance

