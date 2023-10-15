from pages.page import Page
from PIL import Image, ImageDraw
import socket
import util.net_util as net_util

class InfoPage(Page):

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)
        self._name = "Host Info"

    def getImage(self) -> Image:
        newImage = Image.new("1", (self._size[0], self._size[1]))
        draw = ImageDraw.Draw(newImage)
        hostname = socket.gethostname()
        ip_address = net_util.get_ip_address()
        draw.text((draw.textsize(hostname, font=self.font_xl)[0]/2, 3), text=hostname, fill='white', font=self.font_xl)
        draw.text((0, 22), text=ip_address, fill='white', font=self.font_l)
        return newImage

    def getName(self):
        return self._name