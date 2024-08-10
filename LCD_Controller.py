from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import time
import third_party.ILI9486 as LCD
import legacy.config as config
import random
import cv2
import numpy as np


spi: SpiDev = None

class LCD_Controller:
    def __init__(self, spi)->None:
        self.lcd_size = (480, 320)
        self.spi = spi
        self.spi.mode = 0b10
        self.spi.max_speed_hz = 64000000

        self.lcd = LCD.ILI9486(dc=5, rst=6, spi=self.spi).begin()
        self.lcd = LCD.ILI9486(dc=config.DC_PIN, rst=config.RST_PIN, spi=spi).begin()
        print(f'Initialized display with landscape mode = {self.lcd.is_landscape()} and dimensions {self.lcd.dimensions()}')
        
    def generate_img(self, rgb_color: tuple, grid_size:int) -> Image:
        img = Image.new('RGB', self.lcd_size, rgb_color)
        # Split the image into a grid
        for x in range(0, self.lcd_size[0], grid_size):
            for y in range(0, self.lcd_size[1], grid_size):
                img.putpixel((x, y), rgb_color)
                
        return img
    
    def generate_random_img(self, grid_size:int) -> Image:
        img = Image.new('RGB', self.lcd_size)
        # Split the image into a grid
        for x in range(0, self.lcd_size[0], grid_size):
            for y in range(0, self.lcd_size[1], grid_size):
                random_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                for i in range(x, min(x + grid_size, self.lcd_size[0])):
                    for j in range(y, min(y + grid_size, self.lcd_size[1])):
                        img.putpixel((i, j), random_color)
        img = np.array(img)
        res_img = cv2.resize(img,(500,500),interpolation=cv2.INTER_NEAREST)
        cv2.imshow("LCD", np.array(res_img))
        cv2.waitKey(0)
        return img
    
    # def address_grid_8(x:int, y:int, rgb:tuple)->None:
    
    def display_img(self, img: Image) -> None:
        self.lcd.display(img)
        
    def _clear(self) -> None:
        img_clear = Image.new('RGB', self.lcd_size, (0, 0, 0))
        self.lcd.display(img_clear)
        
        
if __name__ == '__main__':
    try:
        GPIO.setmode(GPIO.BCM)
        spi = SpiDev(config.SPI_BUS, config.SPI_DEVICE)
        spi1 = SpiDev(1, 1)
        lcd_control_1 = LCD_Controller(spi=spi)
        lcd_control_2 = LCD_Controller(spi=spi1)
        red_color = (255,255,255)
        while True:
            lcd_control_1.display_img(lcd_control_1.generate_img(red_color,8))
            lcd_control_2.display_img(lcd_control_2.generate_img(red_color,8))
            time.sleep(1)
    except KeyboardInterrupt:
        # catching keyboard interrupt to exit, but do the cleanup in finally block
        pass
    finally:
        lcd_control_1._clear()
        lcd_control_1.lcd.clear().display()
        lcd_control_2._clear()
        lcd_control_2.lcd.clear().display()
        GPIO.cleanup()
        spi.close()
        spi1.close()
