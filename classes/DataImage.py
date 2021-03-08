from abc import ABC, abstractproperty, abstractmethod
import pandas as pd
from pathlib import Path
import classes.Prediction as Prediction
from PIL import Image


class DataImage(ABC):
    @abstractmethod
    def getCaption(self):
        pass


class ImageByPerson(DataImage):
    def __init__(self, person, id):
        self.id = id
        self.filepath = person.img_folder.joinpath(f"Person{person.id}_{id}")
        self.predictions = []

        self.getPredictions()

    def getCaption(self):
        return f"Image by person {self.id}"

    def getPredictions(self):
        predictions = pd.array([])
        try:
            predictions = self.getPredictionsFromCSV()
        except FileNotFoundError:
            try:
                predictions = self.getPredictionsFromTxt()
            except:
                pass

        for row in predictions.iterrows():
            # TODO
            row[1].x

    def getPredictionsFromCSV(self):
        predictions = pd.read_csv(self.filepath.__str__() + '.csv')

        image_size = Image.open(self.filepath.__str__() + '.jpg').size


        predictions['x'] = pd.to_numeric(predictions['x'])/image_size[0]
        predictions['y'] = pd.to_numeric(predictions['y'])/image_size[1]

        return predictions

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
