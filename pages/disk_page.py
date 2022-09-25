import math
import threading
from time import sleep
from PIL import Image
from pages.page import Page
import psutil
import display

class DiskPage(Page):

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)
        self._name = "Disk"
        self.dsk_load = 0
        self.dsk_used = 0
        threading.Thread(name='Disk Load Watchdog',
                         target=self.watchLoad, daemon=True).start()

    def getImage(self) -> Image:
        self.img = Image.new("1", size=self._size)
        self.drawGauge('DISK',
                       (self.img.width / 2, self.img.height / 3 + 10),
                       30, 0, 100, self.dsk_load, min_degrees=170, max_degrees=370, valueLabel='%s GB' % self.dsk_used)
        return self.img

    def getName(self):
        return self._name

    def watchLoad(self):
        while True:
            dsk_virt = psutil.disk_usage('/')
            self.dsk_load = dsk_virt.percent
            self.dsk_used = math.floor(dsk_virt.used / 1024 / 1024 / 1024 * 100) / 100
            sleep(display.REFRESH_RATE)