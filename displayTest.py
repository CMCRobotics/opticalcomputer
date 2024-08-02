import board
import digitalio
from PIL import Image
import adafruit_ili9341
import adafruit_rgb_display.spi as rgb
import numpy as np

# Configuration for CS and DC pins (these can vary depending on your setup)
cs_pin = digitalio.DigitalInOut(board.D8)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (usually 24mhz)
baudrate = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display object:
display = adafruit_ili9341.ILI9341(
    spi, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=baudrate
)

# Generate an example array of RGB values
# Let's say you have a 320x240 image
width, height = 320, 240
rgb_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

# Convert the array to an Image object
image = Image.fromarray(rgb_array, 'RGB')

# Display the image on the LCD
display.image(image)
