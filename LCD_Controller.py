from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import time
import third_party.ILI9486 as LCD
import legacy.config as config

spi: SpiDev = None

class LCD_Controller:
    def __init__(self) -> None:
        self.lcd_size = (480, 320)
        try:
            GPIO.setmode(GPIO.BCM)
            spi = SpiDev(config.SPI_BUS, config.SPI_DEVICE)
            spi.mode = 0b10  # [CPOL|CPHA] -> polarity 1, phase 0
            spi.max_speed_hz = 64000000
            self.lcd = LCD.ILI9486(dc=config.DC_PIN, rst=config.RST_PIN, spi=spi).begin()
            print(f'Initialized display with landscape mode = {self.lcd.is_landscape()} and dimensions {self.lcd.dimensions()}')
        except Exception as e:
            print(f'Error initializing display: {e}')
            raise e
        finally:
            self._clear()
            GPIO.cleanup()
            spi.close()
        pass
    
    def generate_img(self, rgb_color: tuple, grid_size:int) -> Image:
        img = Image.new('RGB', self.lcd_size, rgb_color)
        # Split the image into a grid
        for x in range(0, self.lcd_size[0], grid_size):
            for y in range(0, self.lcd_size[1], grid_size):
                img.putpixel((x, y), (0, 255, 0))
                
        return img
    
    def display_img(self, img: Image) -> None:
        self.lcd.display(img)
        
    def _clear(self) -> None:
        img_clear = Image.new('RGB', self.lcd_size, (0, 0, 0))
        self.lcd.display(img_clear)

if __name__ == '__main__':
    lcd_controller = LCD_Controller()
    img = lcd_controller.generate_img((255, 0, 0), 8)
    lcd_controller.display_img(img)
    time.sleep(5)
    lcd_controller._clear()
    pass