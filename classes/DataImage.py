from abc import ABC, abstractproperty, abstractmethod
import pandas as pd
from pathlib import Path
from classes.Prediction import Prediction
from classes.BoundingBox import BoundingBox
from PIL import Image
import copy


class DataImage(ABC):
    @abstractmethod
    def getCaption(self):
        pass


class ImageByPerson(DataImage):
    def __init__(self, person, id):
        self.id = id
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
        predictions = pd.array([])
        try:
            predictions = self.getPredictionsFromCSV()
        except FileNotFoundError:
            try:
                predictions = self.getPredictionsFromTxt()
            except:
                pass

        for row in predictions.iterrows():
            bounding_box = BoundingBox(row[1].x, row[1].y, row[1].Width, row[1].Height)
            prediction = Prediction(row[1].Label, row[1].Score, bounding_box)
            self.predictions.append(copy.deepcopy(prediction))

    def getPredictionsFromCSV(self):
        predictions = pd.read_csv(self.filepath.__str__() + '.csv')

        self.makeCoordinatesRelative(predictions)

        return predictions

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

    def getPredictionsFromTxt(self):
        text_file = open(self.filepath.__str__() + '.txt', 'r')
        lines = text_file.read().split(' ')
        return pd.array([lines])


class ObjectImage(DataImage):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def getCaption(self):
        return f"Image {self.id} of a {self.name}"
