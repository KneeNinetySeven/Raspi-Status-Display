import threading
from PIL import Image, ImageDraw

ARC_LEN = 270
MARGIN = 5

class LoadingScreen:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.angle = 0

    def cycleLoading(self) -> Image:
        img = Image.new("1", (self.width, self.height))
        draw = ImageDraw.Draw(img)
        draw.arc([((self.width / 2) - (self.height / 2) + MARGIN, 0 + MARGIN), 
                    ((self.width / 2) + (self.height / 2) - MARGIN, self.height - MARGIN)],
                    start=self.angle, end=self.angle + ARC_LEN, fill='white', width=2)
        self.angle += 15
        return img