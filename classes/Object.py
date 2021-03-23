from pathlib import Path
import copy
import classes.DataImage as DataImage


class Object:
    def __init__(self, name, filepath):
        self.name = name
        self.filepath = filepath
        self.images = []

        self.__setImages()

    def __str__(self):
        return self.name

    def __setImages(self):
        for image_id in self.__getImageIds():
            self.images.append(DataImage.ObjectImage(image_id, self))

    def __getImageIds(self):
        img_ids = [folder.stem.replace(f'{self.name}_', '') for folder in self.filepath.iterdir()
                   if folder.match(f'{self.name}_*.jpg')]
        img_ids.sort()

        return img_ids


def getObjects():
    data_folder = Path("../2AMV10/data/raw/trainingImages/")
    object_names = [folder.stem for folder in data_folder.iterdir() if not folder.match('*.DS*')]
    object_names.sort()

    objects = []
    for object_name in object_names:
        temp_object = Object(object_name, data_folder.joinpath(object_name))
        objects.append(copy.deepcopy(temp_object))

    return objects
