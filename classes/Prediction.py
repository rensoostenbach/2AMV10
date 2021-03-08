import classes.BoundingBox as BoundingBox

class Prediction:
    def __init__(self, label, score, bounding_box):
        self.label = label
        self.score = score
        self.bounding_box = bounding_box

    def __str__(self):
        return f"Label: {self.label}, score: {self.score}, bounding box: {self.bounding_box.__str__()}"