import logging
import math
import string
import threading
from time import sleep
from PIL import Image
from pages.page import Page

class TemperaturePage(Page):

    def __init__(self, size: tuple[int, int]) -> None:
        super().__init__(size)
        self._name = "CPU Temp"
        self.tempStr = "0"
        threading.Thread(name='CPU Temp Watchdog', target=self.watchTemp, daemon=True).start()

    def getImage(self) -> Image:
        self.img = Image.new("1", (self._size[0], self._size[1]))
        self.drawLinearGauge('', [(2,2), (self.img.width, self.img.height - 20)], 20, 110, self.getCPUTemp(), 'horizontal', valueLabel='%s°C' % self.getCPUTemp())
        return self.img

    def getName(self) -> string: 
        return self._name

    def getCPUTemp(self): 
        return math.floor(int(self.tempStr) / 100) / 10
    
    def loadTempFromSys(self): 
        try:
            self.tempStr = open('/sys/class/thermal/thermal_zone0/temp', 'r').read().replace('\n', '')
        except Exception:
            self.tempStr = "0"
    
    def watchTemp(self): 
        while True: 
            self.loadTempFromSys()
            logging.debug('Read temperature: %s' %(self.tempStr))
            sleep(2.5)
