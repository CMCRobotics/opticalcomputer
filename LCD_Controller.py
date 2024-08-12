from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import time
import third_party.ILI9486 as LCD
import legacy.config as config
import random
import cv2
import numpy as np

class LCD_Controller:
    def __init__(self, spi:SpiDev)->None:
        self.lcd_size = (480, 320)
        self.spi = spi
        self.spi.mode = 0b10
        self.spi.max_speed_hz = 64000000

        self.lcd = LCD.ILI9486(dc=5, rst=6, spi=self.spi).begin()
        self.lcd = LCD.ILI9486(dc=config.DC_PIN, rst=config.RST_PIN, spi=spi).begin()
        print(f'Initialized display with landscape mode = {self.lcd.is_landscape()} and dimensions {self.lcd.dimensions()}')
        
    def generate_img(self, rgb_color: tuple, grid_size:int) -> Image:
        """
        Generates an image with the specified RGB color and grid size.

        Args:
            rgb_color (tuple): The RGB color tuple (R, G, B) to fill the image with.
            grid_size (int): The size of each grid cell in pixels.

        Returns:
            Image: The generated image.

        """
        img = Image.new('RGB', self.lcd_size, rgb_color)
        # Split the image into a grid
        for x in range(0, self.lcd_size[0], grid_size):
            for y in range(0, self.lcd_size[1], grid_size):
                img.putpixel((x, y), rgb_color)
                
        return img
    
    def generate_random_img(self, grid_size:int) -> Image:
        """
        Generates a random image with the specified grid size.

        Parameters:
        - grid_size (int): The size of each grid cell in pixels.

        Returns:
        - img (numpy.ndarray): The generated random image as a NumPy array.

        """
        img = Image.new('RGB', self.lcd_size)
        # Split the image into a grid
        for x in range(0, self.lcd_size[0], grid_size):
            for y in range(0, self.lcd_size[1], grid_size):
                random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for i in range(x, min(x + grid_size, self.lcd_size[0])):
                    for j in range(y, min(y + grid_size, self.lcd_size[1])):
                        img.putpixel((i, j), random_color)
        img = np.array(img)
        return img
    
    def address_grid_8(self, img:Image, x:int, y:int, rgb:tuple)->Image:
        grid_size = self.lcd_size[0] // 8
        top_left_x = 0
        top_left_y = 0
        
        for i in range(top_left_x, top_left_x + grid_size):
            for j in range(top_left_y, top_left_y + grid_size):
                img.putpixel((i, j), rgb)
        return img
    
    def display_img(self, img: Image) -> None:
        self.lcd.display(img)
        
    def _clear(self) -> None:
        img_clear = Image.new('RGB', self.lcd_size, (0, 0, 0))
        self.lcd.display(img_clear)
        
        
if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        spi_lcd_1 = SpiDev(config.SPI_BUS, config.SPI_DEVICE)
        spi_lcd_2 = SpiDev(1, 1)
        lcd_control_1 = LCD_Controller(spi=spi_lcd_1)
        lcd_control_2 = LCD_Controller(spi=spi_lcd_2)
        red_color = (255,0,0)
        while True:
            lcd_control_1.display_img(lcd_control_1.address_grid_8(1,2,red_color))
            img_rot = Image.fromarray(cv2.rotate(np.array(lcd_control_2.address_grid_8(1,1,red_color)),cv2.ROTATE_180))
            lcd_control_2.display_img(lcd_control_2.generate_img((0,0,255),8))
    except KeyboardInterrupt:
        pass
    finally:
        lcd_control_1.lcd.clear().display()
        lcd_control_2.lcd.clear().display()
        GPIO.cleanup()
        spi_lcd_1.close()
        spi_lcd_2.close()
