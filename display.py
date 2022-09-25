import logging
import math
from time import sleep
import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pages.info_page import InfoPage
from pages.load_page import LoadPage
from loading_screen import LoadingScreen
from pages.page import Page

from pages.temp_page import TemperaturePage

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

WIDTH = 128
HEIGHT = 64
BORDER = 5

CYCLES_PER_PAGE = 50

i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)

activePages = [
    InfoPage((oled.width, oled.height)),
    TemperaturePage((oled.width, oled.height)),
    LoadPage((oled.width, oled.height)),
]

font = ImageFont.truetype("Ubuntu-Bold.ttf", size=12)

def run():
    logging.info('Starting monitor')
    loadingScreen = LoadingScreen(oled)
    running = True
    sleep(10)

    cycle = 0
    pageIndex = 0
    
    loadingScreen.dispose()
    
    try:
        while running:
            currentPage = activePages[pageIndex]

            # Display image
            logging.debug('Loading image')
            image = drawFooter(currentPage, pageIndex, len(
                activePages), cycle, CYCLES_PER_PAGE, currentPage.getImage())
            oled.image(image)
            oled.show()

            logging.debug('Hibernating...')

            cycle += 1
            if (cycle % CYCLES_PER_PAGE == 0):
                cycle = 0
                pageIndex = (pageIndex + 1) if (pageIndex +
                                                1) < len(activePages) else 0
            logging.debug('Cycle %s // NextPage: %s' %
                          (cycle, activePages[pageIndex].getName()))
            sleep(.1)

    except InterruptedError:
        logging.info('OK guys. We\'ve been interrupted!')
        currentPage.finished = True
        running = False
        sendToSleep()


def drawFooter(page: Page, index, activePages, currentCycle, maxCycles, image: Image) -> Image:
    draw = ImageDraw.Draw(image)
    strokeWidth = 1
    footerOffset = 16
    footerTextOffsetLeft = 3
    draw.line([(0, image.height - footerOffset), (image.width,
              image.height - footerOffset)], 'white', width=strokeWidth,)
    draw.line([(0, image.height - footerOffset), (image.width * (currentCycle /
              maxCycles), image.height - footerOffset)], 'white', width=strokeWidth*3,)
    draw.line([(math.floor(image.width/2), image.height - footerOffset),
              (math.floor(image.width/2), image.height)], 'white', width=strokeWidth,)

    draw.text((0 + footerTextOffsetLeft, image.height - draw.textsize(page.getName())
              [1] - footerTextOffsetLeft), page.getName(), 'white', font=font)

    dotOffsetX = (image.width / 2)
    dotSpacingX = (image.width / 2 / activePages)

    dotSize = min([footerOffset - 8, dotSpacingX - 6])

    for dotNum in range(activePages):
        xBoundaryLeft = dotOffsetX + \
            (dotSpacingX / 2) + (dotNum * dotSpacingX) - dotSize/2
        xBoundaryRight = dotOffsetX + \
            (dotSpacingX / 2) + (dotNum * dotSpacingX) + dotSize/2
        bounds = [(xBoundaryLeft,  image.height - (footerOffset/2) - (dotSize / 2)),
                  (xBoundaryRight, image.height - (footerOffset/2) + (dotSize / 2))]

        if dotNum == index:
            logging.debug('Drawing %s filled' % dotNum)
            draw.pieslice(bounds, 0, 359, fill='white')
        else:
            logging.debug('Drawing %s empty' % dotNum)
            draw.arc(bounds, 0, 359, fill='white', width=1)

    return image


def sendToSleep(self, *args):
    sleepImg = Image.open('sleep.png')
    sleepImg = sleepImg.convert('1')
    sleepImg = sleepImg.resize((64, 64))
    sleepImg = ImageChops.invert(sleepImg)
    img = Image.new('1', (oled.width, oled.height))
    img.paste(sleepImg, (int((img.width / 2) - (sleepImg.width / 2)), int((img.height / 2) - (sleepImg.height/2))))
    oled.image(img)
    oled.show()

    quit()

