import string
from PIL import Image, ImageDraw, ImageChops, ImageFont

class Page:

    def __init__(self, size: tuple[int, int]) -> None:
        self._size = size
        self.font_xl = ImageFont.truetype("Ubuntu-Bold.ttf", size=18)
        self.font_l = ImageFont.truetype("Ubuntu-Bold.ttf", size=14)
        self.font_s = ImageFont.truetype("Ubuntu-Bold.ttf", size=8)

    def getImage() -> Image: 
        pass

    def getName() -> string: 
        pass

    def drawGauge(self, name, center, size, min, max, val, min_degrees=140, max_degrees=400, valueLabel=None):
        draw = ImageDraw.Draw(self.img)
        val_degrees = self.translate(val, min, max, min_degrees, max_degrees)
        draw.pieslice([(center[0] - size, center[1] - size),
                      (center[0] + size, center[1] + size)],
                      min_degrees, max_degrees, outline='white', width=1)
        draw.pieslice([(center[0] - size, center[1] - size),
                      (center[0] + size, center[1] + size)],
                      min_degrees, val_degrees, fill='white', width=1)

        textImg = Image.new("1", size=self._size)
        textDraw = ImageDraw.Draw(textImg)
        if valueLabel is None:
            text = '%s%%' % val
        else:
            text = valueLabel
        textDraw.text((center[0]-(draw.textsize(text)[0] / 2), center[1] - 15),
                      text, fill='white', font=self.font_l)
        textDraw.text((center[0]-10, center[1]+5),
                      name, fill='white', font=self.font_s)

        self.img = ImageChops.logical_xor(self.img, textImg)

    def drawLinearGauge(self, name, bounds: list[tuple[int, int]], min, max, val, direction, valueLabel=None):
        innerBorder = 3

        draw = ImageDraw.Draw(self.img)
        draw.rounded_rectangle(bounds, radius=4, fill='black', outline='white', width=2)
        
        if direction == 'horizontal':
            innerBounds = ((bounds[0][0] + innerBorder, bounds[0][1] + innerBorder), (self.translate(val, min, max, 0, bounds[1][0] - innerBorder), bounds[1][1] - innerBorder))
        else: 
            innerBounds = ((bounds[0][0] + innerBorder,  self.translate(val, min, max, bounds[1][1] - innerBorder, bounds[0][1] + innerBorder)), (bounds[1][0] - innerBorder, bounds[1][1] - innerBorder))
        if val > min: draw.rounded_rectangle(innerBounds, radius=2, fill='white', outline='white', width=2)

        textImg = Image.new("1", size=self._size)
        textDraw = ImageDraw.Draw(textImg)
        if valueLabel is None:
            value = '%s%%' % val
        else:
            value = valueLabel
        center = ((bounds[1][0] - bounds[0][0]) / 2, (bounds[1][1] - bounds[0][1]) / 2)
        textDraw.text((center[0]- (draw.textsize(value)[0] / 2), center[1] - (draw.textsize(value)[1] / 2)),
                      value, fill='white', font=self.font_xl)
        textDraw.text((center[0]- (draw.textsize(value)[0] / 2), bounds[1][1]),
                      name, fill='white', font=self.font_l)

        self.img = ImageChops.logical_xor(self.img, textImg)

    
    def translate(self, val, in_min, in_max, out_min, out_max):
        return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
