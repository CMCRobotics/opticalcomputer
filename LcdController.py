from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import time
from .third_party import ILI9486 as LCD

class PinConfig():
    # Pin definition
    RST_PIN = 25
    DC_PIN = 24
    # SPI definition
    SPI_BUS = 0
    SPI_DEVICE = 0

class LcdController():
    def __init__(self):
        self.spi = SpiDev(PinConfig.SPI_BUS, PinConfig.SPI_DEVICE)

        GPIO.setmode(GPIO.BCM)
        self.spi.mode = 0b10  # [CPOL|CPHA] -> polarity 1, phase 0
        # default value
        # spi.lsbfirst = False  # set to MSB_FIRST / most significant bit first
        self.spi.max_speed_hz = 64000000
        lcd = LCD.ILI9486(dc=PinConfig.DC_PIN, rst=PinConfig.RST_PIN, spi=self.spi).begin()
        print(f'Initialized display with landscape mode = {lcd.is_landscape()} and dimensions {lcd.dimensions()}')
        print('Loading image...')
        image = Image.open('sample.png')
        width, height = image.size
        partial = image.resize((width // 2, height // 2))

        while True:
            lcd.display(image)

    def close(self):
        GPIO.cleanup()
        self.spi.close()
