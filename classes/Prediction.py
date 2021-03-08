import classes.BoundingBox as BoundingBox

class Prediction:
    def __init__(self, prediction_label, score, bounding_box):
        self.prediction_label = prediction_label
        self.score = score
        self.bounding_box = bounding_box