import string
import qrcode
from PIL import Image, ImageDraw, ImageChops
import logging
from pages.page import Page

class QRCodePage(Page):
    def __init__(self, size: tuple[int, int], name: str, content: str) -> None:
        super().__init__(size)
        self.name = name
        self.img : Image = qrcode.make(data=content)
        self.img = self.img.resize((55, 55))
        self.img = ImageChops.invert(self.img)

        self.logger = logging.getLogger("QR Code Page")
        self.logger.debug(self.img.size)

    def getName(self) -> str:
        return self.name

    def getImage(self) -> Image:
        newImage = Image.new("1", (self._size[0], self._size[1]))
        newImage.paste(
            self.img,
            (
                int((newImage.width / 2) - (self.img.width / 2)),
                -5
            ),
        )
        return newImage