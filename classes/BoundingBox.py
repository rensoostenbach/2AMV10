class BoundingBox():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f'(x,y) = ({self.x}, {self.y}), (width, height) = ({self.width}, {self.height})'

    def getCoordinates(self):
        return (self.x, self.y), (self.x+self.width, self.y+self.height)

