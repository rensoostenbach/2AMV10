from abc import ABC, abstractmethod

class BoundingBox(ABC):
    @abstractmethod
    def getCoordinates(self):
        pass


class fixedBoundingBox(BoundingBox):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def getCoordinates(self):
        return (self.x, self.y), (self.x+self.width, self.y+self.height)


class RelativeBoundingBox(BoundingBox):
    def __init__(self, x):
        self.x = x