import copy

from sklearn.cluster import KMeans

import classes.DataImage as DataImage
from pathlib import Path
import numpy as np
import pandas as pd


class Person:
    def __init__(self, id, folder):
        self.id = id
        self.img_folder = folder
        self.images = []
        self.cluster = None

        self.setImages()

    def __str__(self):
        return f'Person {self.id}'

    def setImages(self):
        for image_id in self.__getImageIds():
            self.images.append(DataImage.ImageByPerson(image_id, self))

    def getImage(self, image_id):
        for image in self.images:
            if image.id == image_id:
                return image

        return None

    def __getImageIds(self):
        img_ids = [folder.stem.replace(f'Person{self.id}_', '') for folder in self.img_folder.iterdir()
            if folder.match(f'Person{self.id}_*.jpg')]
        img_ids.sort()

        return img_ids


def getPersonsFrom(data_folder, objects, k):
    person_ids = getPersonIdsFrom(data_folder)
    persons = []
    persons_with_total_item_scores = pd.DataFrame(0, index=np.arange(40), columns=[obj.name for obj in objects])

    for person_id in person_ids:
        img_folder = __getImgFolder(data_folder, person_id)
        new_person = Person(person_id, img_folder)
        for img in new_person.images:
            for prediction in img.predictions:
                persons_with_total_item_scores.loc[int(new_person.id) - 1, prediction.label] += prediction.score
        persons.append(copy.deepcopy(new_person))

    kmeans = KMeans(n_clusters=k)
    kmeans.fit(persons_with_total_item_scores)

    for person in persons:
        person.cluster = kmeans.predict(persons_with_total_item_scores.loc[int(person.id) - 1].values.reshape(1, -1))
        if person.cluster == 1:
            print(persons_with_total_item_scores.loc[int(person.id) - 1].values.reshape(1, -1))

    return persons


def getPersonIdsFrom(data_folder):
    person_ids = [folder.stem.replace('Person', '') for folder in data_folder.iterdir() if folder.match('Person*')]

    for i, person_id in enumerate(person_ids):
        idx = person_id.find('_')
        if idx != -1:
            person_ids[i] = person_id[:idx]

    return np.unique(person_ids)


def getPersonFrom(person_id, data_folder):
    img_folder = __getImgFolder(data_folder, person_id)
    new_person = Person(person_id, img_folder)

    return copy.deepcopy(new_person)


def __getImgFolder(data_folder, person_id):
    if data_folder == Path("../2AMV10/data/raw/"):
        data_folder = data_folder.joinpath(f'Person{person_id}/')

    return data_folder
