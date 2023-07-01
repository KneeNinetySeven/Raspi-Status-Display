import logging
import logging.handlers
import math
from time import sleep, time
from dateutil import parser
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont, ImageChops
from pages.disk_page import DiskPage
from pages.info_page import InfoPage
from pages.load_page import LoadPage
from util.loading_screen import LoadingScreen
from util.time_utils import in_between
from pages.page import Page

from pages.temp_page import TemperaturePage

IS_MOCKED = True

WIDTH = 128
HEIGHT = 64
BORDER = 5

REFRESH_RATE = 0.5
MILLIS_PER_PAGE = 20000

activePages = [
    InfoPage((WIDTH, HEIGHT)),
    LoadPage((WIDTH, HEIGHT)),
    DiskPage((WIDTH, HEIGHT)),
    TemperaturePage((WIDTH, HEIGHT)),
]

font = ImageFont.truetype("Ubuntu-Bold.ttf", size=12)

OLED = None

def run(config):
    IS_MOCKED = config["display"].getboolean("mocked", fallback=True)
    MILLIS_PER_PAGE = config["display"].getint("page_duration_millis", fallback=20000)

    logger = logging.getLogger()
    logger.info("Starting monitor")

    if not IS_MOCKED:
        import board
        import busio
        import adafruit_ssd1306

        i2c = busio.I2C(board.SCL, board.SDA)
        OLED = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
    else:
        logger.info(
            "Status display is running mocked up and will only display output.bmp"
        )
    
    loadingScreen = LoadingScreen(WIDTH, HEIGHT)
    for _ in range(100):
        img = loadingScreen.cycleLoading()
        if not IS_MOCKED:
            OLED.image(img)
            OLED.show()
        else: 
            img.save("output.bmp")
        sleep(.05)

    running = True

    lastCycleMillis = get_current_time_millis()
    pageIndex = 0
    try:
        image = Image.new("1", (WIDTH, HEIGHT))
        while running:
            if config["display"].getboolean('auto_off_enabled') and in_between(
                datetime.now(),
                parser.parse(config["display"]["auto_off"]),
                parser.parse(config["display"]["auto_on"]),
            ):
                image = loadingScreen.cycleLoading()
            else: 
                currentPage = activePages[pageIndex]

                # Display image
                logger.debug("Loading image")
                image = currentPage.getImage()
                image = drawFooter(
                    currentPage,
                    pageIndex,
                    len(activePages),
                    get_current_time_millis() - lastCycleMillis,
                    MILLIS_PER_PAGE,
                    image,
                )

            if IS_MOCKED:
                image.save("output.bmp")
            else:
                OLED.image(image)
                OLED.show()

            logger.debug("Awaiting next frame...")

            if get_current_time_millis() - lastCycleMillis >= MILLIS_PER_PAGE:
                logger.info(
                    "Millis passed %s // NextPage: %s"
                    % (
                        get_current_time_millis() - lastCycleMillis,
                        activePages[pageIndex].getName(),
                    )
                )
                pageIndex = (pageIndex + 1) if (pageIndex + 1) < len(activePages) else 0
                lastCycleMillis = get_current_time_millis()

            sleep(0.5)

    except InterruptedError:
        logger.info("OK guys. We've been interrupted!")
        currentPage.finished = True
        running = False
        sendToSleep()


def get_current_time_millis():
    return round(time() * 1000)


def drawFooter(
    page: Page, index, activePages, currentMicros, targetMicros, image: Image
) -> Image:
    draw = ImageDraw.Draw(image)
    strokeWidth = 1
    footerOffset = 16
    footerTextOffsetLeft = 3
    draw.line(
        [(0, image.height - footerOffset), (image.width, image.height - footerOffset)],
        "white",
        width=strokeWidth,
    )
    draw.line(
        [
            (0, image.height - footerOffset),
            (image.width * (currentMicros / targetMicros), image.height - footerOffset),
        ],
        "white",
        width=strokeWidth * 3,
    )
    draw.line(
        [
            (math.floor(image.width / 2), image.height - footerOffset),
            (math.floor(image.width / 2), image.height),
        ],
        "white",
        width=strokeWidth,
    )

    draw.text(
        (
            0 + footerTextOffsetLeft,
            image.height - draw.textsize(page.getName())[1] - footerTextOffsetLeft,
        ),
        page.getName(),
        "white",
        font=font,
    )

    dotOffsetX = image.width / 2
    dotSpacingX = image.width / 2 / activePages

    dotSize = min([footerOffset - 8, dotSpacingX - 6])

    for dotNum in range(activePages):
        xBoundaryLeft = (
            dotOffsetX + (dotSpacingX / 2) + (dotNum * dotSpacingX) - dotSize / 2
        )
        xBoundaryRight = (
            dotOffsetX + (dotSpacingX / 2) + (dotNum * dotSpacingX) + dotSize / 2
        )
        bounds = [
            (xBoundaryLeft, image.height - (footerOffset / 2) - (dotSize / 2)),
            (xBoundaryRight, image.height - (footerOffset / 2) + (dotSize / 2)),
        ]

        if dotNum == index:
            logging.debug("Drawing %s filled" % dotNum)
            draw.pieslice(bounds, 0, 359, fill="white")
        else:
            logging.debug("Drawing %s empty" % dotNum)
            draw.arc(bounds, 0, 359, fill="white", width=1)

    return image


def sendToSleep(self, *args):
    logging.getLogger().info("Going into sleep mode.")

    img = getSleepingImage()
    if IS_MOCKED:
        img.save("output.bmp")
    else:
        OLED.image(img)
        OLED.show()

    quit()

def getSleepingImage() -> Image:
    sleepImg = Image.open("img/sleep.png")
    sleepImg = sleepImg.convert("1")
    sleepImg = sleepImg.resize((64, 64))
    sleepImg = ImageChops.invert(sleepImg)
    img = Image.new("1", (WIDTH, HEIGHT))
    img.paste(
        sleepImg,
        (
            int((img.width / 2) - (sleepImg.width / 2)),
            int((img.height / 2) - (sleepImg.height / 2)),
        ),
    )
    return img