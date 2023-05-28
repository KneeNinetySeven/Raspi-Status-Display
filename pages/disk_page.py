import math
import threading
from time import sleep
from PIL import Image
from pages.page import Page
import psutil
import display
import os

class DiskPage(Page):

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)
        self._name = "Disk"
        self.dsk_load = {}
        self.dsk_used = {}
        threading.Thread(name='Disk Load Watchdog',
                         target=self.watchLoad, daemon=True).start()

    def getImage(self) -> Image:
        self.img = Image.new("1", size=self._size)
        partCount = len(self.dsk_used.items())
        index = 0
        for partition in self.dsk_used:
            size = (self.img.width / partCount / 2) - 3
            self.drawGauge(os.path.basename(partition), (((self.img.width / partCount) * index) + (self.img.width / partCount / 2), self.img.height / 3 + 10),
                           size, 0, 100, self.dsk_load[partition],
                           min_degrees=170, max_degrees=370,
                           valueLabel='%s GB' % self.dsk_used[partition])
            index += 1
        return self.img

    def getName(self):
        return self._name

    def watchLoad(self):
        while True:
            partitions = psutil.disk_partitions()
            dsk_used = {}
            dsk_load = {}
            for partition in partitions:
                dsk_virt = psutil.disk_usage(partition.mountpoint)
                dsk_load[partition.device] = dsk_virt.percent
                dsk_used[partition.device] = math.floor(dsk_virt.used / 1024 / 1024 / 1024 * 100) / 100
            self.dsk_used = dsk_used
            self.dsk_load = dsk_load
            sleep(display.REFRESH_RATE * 5)
