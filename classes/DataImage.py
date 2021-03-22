from abc import ABC, abstractproperty, abstractmethod
import pandas as pd
from pathlib import Path
from classes.Prediction import Prediction
from classes.BoundingBox import BoundingBox
from PIL import Image
import numpy as np
import copy
import cv2
from math import ceil

COLORS = [
    (123, 140, 191),
    (0, 0, 0),
    (244, 205, 83),
    (0, 0, 255),
    (128, 169, 128),
    (170, 175, 140),
    (205, 181, 169),
    (120, 110, 125),
    (41, 43, 81),
    (183, 172, 140),
    (0, 255, 0),
    (255, 0, 0)
]


class DataImage(ABC):
    def __init__(self, id):
        self.id = id
        self.filepath = ''

    def get(self):
        return Image.open(self.filepath)

    @abstractmethod
    def getCaption(self):
        pass


class ImageByPerson(DataImage):
    def __init__(self, id, person):
        super().__init__(id)

        self.person = person
        self.filepath = person.img_folder.joinpath(f"Person{person.id}_{id}")
        self.predictions = []

        self.setPredictions()

        self.filepath = str(self.filepath) + '.jpg'

    def __str__(self):
        return f'Image {self.id}'

    def getCaption(self):
        return f"Image {self.id} by person {self.person.id}"

    def setPredictions(self):
        predictions = self.getPredictionsFromFile()

        for i, row in enumerate(predictions.iterrows()):
            bounding_box = BoundingBox(row[1].x, row[1].y, row[1].Width, row[1].Height, COLORS[i % len(COLORS)])
            prediction = Prediction(row[1].Label, row[1].Score, bounding_box)
            self.predictions.append(copy.deepcopy(prediction))

    def getPredictionsFromFile(self):
        predictions = pd.DataFrame()

        try:
            predictions = self.getPredictionsFromCSV()
        except FileNotFoundError:
            try:
                predictions = self.getPredictionsFromTxt()
            except:
                pass

        return predictions

    def getPredictionsFromCSV(self):
        predictions = pd.read_csv(self.filepath.__str__() + '.csv')

        self.makeCoordinatesRelative(predictions)
        predictions = self.__formatPredictionsDataframe(predictions)

        return predictions[predictions['Score'] >= 0.085]

    def getPredictionsFromTxt(self):
        label_path = self.filepath.parents[0]

        if label_path.joinpath('labels').exists():
            label_path = label_path.joinpath('labels')

        predictions = pd.DataFrame()

        for file in label_path.iterdir():
            if file.match(f'Person{self.person.id}_{self.id}*.txt'):
                predictions = pd.read_table(file, delim_whitespace=True,
                                            names=('Label', 'x', 'y', 'Width', 'Height', 'Score'))
                pd.to_numeric(predictions['Score'])

        predictions = self.__formatBoundingBoxCoordinates(predictions)

        return predictions[predictions['Score'] >= 0.085]

    def makeCoordinatesRelative(self, predictions):
        image_size = Image.open(self.filepath.__str__() + '.jpg').size
        try:
            predictions['x'] = pd.to_numeric(predictions['x']) / image_size[0]
            predictions['y'] = pd.to_numeric(predictions['y']) / image_size[1]
            predictions['Width'] = pd.to_numeric(predictions['Width']) / image_size[0]
            predictions['Height'] = pd.to_numeric(predictions['Height']) / image_size[0]
        except:
            predictions['x'] = 0
            predictions['y'] = 0
            predictions['Width'] = pd.to_numeric(predictions['Width']) / image_size[0]
            predictions['Height'] = pd.to_numeric(predictions['Height']) / image_size[0]

    def __formatPredictionsDataframe(self, predictions):
        while predictions.shape[1] < 6:
            predictions[predictions.shape[1]] = 0

        predictions.columns=['x', 'y', 'Width', 'Height', 'Score', 'Label']

        return predictions

    def __formatBoundingBoxCoordinates(self, predictions):
        if self.__isYoloModel():
            predictions['x'] -= predictions['Width']/2
            predictions['y'] -= predictions['Height']/2
        else:
            predictions.rename(columns={'x': 'y', 'y': 'x', 'Width': 'Height', 'Height': 'Width'}, inplace=True)
            predictions['Width'] = predictions['Width'] - predictions['x']
            predictions['Height'] = predictions['Height'] - predictions['y']

        return predictions

    def getImageWithBoundingBoxesWithPredictionScoreAbove(self, confidence_threshold):
        valid_predictions = [prediction for prediction in self.predictions if prediction.score >= confidence_threshold]

        with Image.open(self.filepath) as image:
            return self.__drawBoundingBoxesForPredictionsOn(image, valid_predictions)

    def __drawBoundingBoxesForPredictionsOn(self, image, valid_predictions):
        image_as_array = np.asarray(image)
        image_in_cv2_format = cv2.cvtColor(image_as_array, cv2.COLOR_RGB2BGR)

        if not self.__isYoloModel(): # Yolo models have bounding boxes already drawn (only if the model predicts any)
            self.__drawAllBoundingBoxesAndPredictionsOn(image_in_cv2_format, valid_predictions)

        image_as_array = cv2.cvtColor(image_in_cv2_format, cv2.COLOR_BGR2RGB)
        return Image.fromarray(image_as_array)

    def __drawAllBoundingBoxesAndPredictionsOn(self, image, valid_predictions):
        for index, prediction in enumerate(valid_predictions):
            self.__drawBoundingBoxAndPredictionOn(image, prediction)

    def __drawBoundingBoxAndPredictionOn(self, image, prediction):
        pt1, pt2 = prediction.bounding_box.getIntegerCoordinates(image)

        self.__drawBoundingBoxOn(image, prediction.bounding_box.color, pt1, pt2)

        self.__drawPredictionOn(image, prediction.bounding_box.color, prediction,
                                prediction.bounding_box.getBottomLeftIntegerCoordinate(image))

    def __drawBoundingBoxOn(self, image, color, top_left, top_right):
        thickness = ceil(image.shape[1] / 250)

        cv2.rectangle(image, top_left, top_right, color, thickness)

    def __drawPredictionOn(self, image, color, prediction, bottom_left):
        cv2.putText(
            img=image,
            text=f"{prediction.label}: {prediction.score}",
            org=bottom_left,
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=image.shape[1] / 1000,
            color=color,
            thickness=ceil(image.shape[1] / 500),
        )

    def __isYoloModel(self):
        if isinstance(self.filepath, str):
            self.filepath = Path(self.filepath)

        parents = self.filepath.parents

        for parent in parents:
            if parent.match('*yolo*'):
                return True

        return False


class ObjectImage(DataImage):
    def __init__(self, id, object):
        super().__init__(id)

        self.object = object
        self.filepath = Path("../2AMV10/data/raw/trainingImages/" + object.name + "/" + object.name + "_" + str(id) + '.jpg')

    def __str__(self):
        return f"Image {self.id}"

    def getCaption(self):
        return f"Image {self.id} of a {self.object.name}"
