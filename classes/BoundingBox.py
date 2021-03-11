class BoundingBox():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return f'(x,y) = ({self.x}, {self.y}), (width, height) = ({self.width}, {self.height})'

    def getRelativeCoordinates(self):
        return (self.x, self.y), (self.x+self.width, self.y+self.height)

    def getIntegerCoordinates(self, image):
        top_left = (int(self.x * image.shape[1]), int(self.y * image.shape[0]))
        bottom_right = (int((self.x+self.width) * image.shape[1]), int((self.y+self.height) * image.shape[0]))

        return top_left, bottom_right

    def getBottomLeftIntegerCoordinate(self, image):
        return int(self.x * image.shape[1]), int((self.y + self.height) * image.shape[0]-20)

