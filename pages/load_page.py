import math
import threading
from time import sleep
from PIL import Image
from pages.page import Page
import psutil


class LoadPage(Page):

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)
        self._name = "Sys Load"
        self.cpu_load = 0
        self.mem_load = 0
        self.mem_used = 0
        threading.Thread(name='CPU Temp Watchdog',
                         target=self.watchLoad, daemon=True).start()

    def getImage(self) -> Image:
        self.img = Image.new("1", size=self._size)
        self.drawGauge('CPU',
                       (self.img.width / 2 - (self.img.width / 4), self.img.height / 3),
                       20, 0, 100, self.cpu_load)
        self.drawGauge('MEM',
                       (self.img.width / 2 + (self.img.width / 4), self.img.height / 3),
                       20, 0, 100, self.mem_load, valueLabel='%s MB' % self.mem_used)
        return self.img

    def getName(self):
        return self._name

    def watchLoad(self):
        while True:
            self.cpu_load = psutil.cpu_percent(interval=1)
            mem_virt = psutil.virtual_memory()
            self.mem_load = mem_virt.percent
            self.mem_used = math.floor(mem_virt.used / 1024 / 1024 * 10) / 10
            sleep(0.25)
