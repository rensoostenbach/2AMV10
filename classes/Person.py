import copy
import classes.DataImage as DataImage
from pathlib import Path
import numpy as np


class Person:
    def __init__(self, id, folder):
        self.id = id
        self.img_folder = folder
        self.images = []

        self.setImages()

    def __str__(self):
        return f'Person {self.id}'

    def setImages(self):
        for image_id in self.__getImageIds():
            self.images.append(DataImage.ImageByPerson(image_id, self))

    def __getImageIds(self):
        img_ids = [folder.stem.replace(f'Person{self.id}_', '') for folder in self.img_folder.iterdir()
            if folder.match(f'Person{self.id}_*.jpg')]

        return img_ids


def getPersonsFrom(data_folder):
    person_ids = __getPersonIdsFrom(data_folder)
    persons = []

    for person_id in person_ids:
        img_folder = __getImgFolder(data_folder, person_id)
        new_person = Person(person_id, img_folder)
        persons.append(copy.deepcopy(new_person))

    return persons


def __getPersonIdsFrom(data_folder):
    person_ids = [folder.stem.replace('Person', '') for folder in data_folder.iterdir() if folder.match('Person*')]

    for i, person_id in enumerate(person_ids):
        idx = person_id.find('_')
        if idx != -1:
            person_ids[i] = person_id[:idx]

    return np.unique(person_ids)


def __getImgFolder(data_folder, person_id):
    if data_folder == Path("../2AMV10/data/raw/"):
        data_folder = data_folder.joinpath(f'Person{person_id}/')

    return data_folder
