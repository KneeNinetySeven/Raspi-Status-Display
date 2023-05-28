import threading
from PIL import Image, ImageDraw

ARC_LEN = 270
MARGIN = 5


class LoadingScreen:

    def __init__(self, oled):
        self.oled = oled
        self.angle = 0
        self.stopped = False
        threading.Thread(name='Loading indicator',
                         target=self.cycleLoading).start()

    def cycleLoading(self):
        while not self.stopped:
            img = Image.new("1", (self.oled.width, self.oled.height))
            draw = ImageDraw.Draw(img)
            draw.arc([((self.oled.width / 2) - (self.oled.height / 2) + MARGIN, 0 + MARGIN), 
                     ((self.oled.width / 2) + (self.oled.height / 2) - MARGIN, self.oled.height - MARGIN)],
                     start=self.angle, end=self.angle + ARC_LEN, fill='white', width=2)
            self.oled.image(img)
            self.oled.show()
            self.angle += 15

    def dispose(self):
        self.stopped = True
