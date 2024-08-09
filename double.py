from PIL import Image
import RPi.GPIO as GPIO
from spidev import SpiDev
import time
import ILI9486 as LCD
import config
import numpy as np

import time
import board
import neopixel
#spi: SpiDev = None

#pixels1 = neopixel.NeoPixel(board.D18, 64, brightness=1)

def set_colour(x=1, y=1, rgb_tuple=(255,0,0)):
	pixels1[x+y*8].fill(rgb_tuple)
	pixels1.show()

def prompt_user():
	# Prompt user
    # Split the input string by commas
	while True:
		try:
			RGB_input = input("Enter RGB values (e.g., 255,0,0): ")
			new_x = int(input("Pixel (x): "))
			new_y = int(input("Pixel (y): "))
			# Split the string into a list of strings and convert to integers
			rgb_values = RGB_input.split(',')
			rgb_tuple = tuple(int(value.strip()) for value in rgb_values)
			
			# Validate that we have exactly 3 values (R, G, B)
			if len(rgb_tuple) != 3:
				raise ValueError("Enter exactly three values separated by commas.")
			return new_x, new_y, rgb_tuple
		
		except ValueError as e:
			print(f"Invalid input: {e}")
			return None



def create_image(color, width, height):
	# Calculate the number of zones in both dimensions
	zone_size_x = width // 8
	zone_size_y = height // 8
	num_zones_x =  8 #zone_size
	num_zones_y =  8 #zone_size
	# Create an empty array for the image
	image_array = np.zeros((height, width, 3), dtype=np.uint8)

	for i in range(num_zones_y):
		for j in range(num_zones_x):
            # Generate a random color for the zone
			random_color = np.random.randint(0, 256, 3, dtype=np.uint8)
	 # Assign the random color to the corresponding zone in the image array
			image_array[i * zone_size_x:(i + 1) * zone_size_x, j * zone_size_y:(j + 1) * zone_size_y] = random_color

	#random_image_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
	# Create a new image with the specified color
	#image = Image.new("RGB", (width, height), color)
#	image = Image.fromarray(random_image_array, 'RGB')
	image = Image.fromarray(image_array, 'RGB')
	# Save the image to the specified file path
	return image


if __name__ == '__main__':
	try:
		GPIO.setmode(GPIO.BCM)
		#GPIO.setup(21,GPIO.SERIAL)
		spi = SpiDev(config.SPI_BUS, config.SPI_DEVICE)
		spi1 = SpiDev(1, 1)
		spi.mode = 0b10  # [CPOL|CPHA] -> polarity 1, phase 0
		spi1.mode = 0b10
		
		# default value
		# spi.lsbfirst = False  # set to MSB_FIRST / most significant bit first
		spi.max_speed_hz = 64000000
		spi1.max_speed_hz = 64000000
		lcd = LCD.ILI9486(dc=24, rst=25, spi=spi).begin()
		lcd1 = LCD.ILI9486(dc=5, rst=6, spi=spi1).begin()
		print(f'Initialized display with landscape mode = {lcd.is_landscape()} and dimensions {lcd.dimensions()}')
		# NEW ###############################################################
		pixels1 = neopixel.NeoPixel(board.D18, 64, brightness=1)
		current_colour = (255, 0, 0)  # Initial color (Red)
		set_colour(current_colour)
		
		print("Press Enter to input new color or type 'exit' to quit.")
		
		while True:
			user_input = input("Press Enter to change colour or 'exit' to quit: ")
			if user_input.lower() == 'exit':
				print("Exiting...")
				break
			
			# Get new colour input
			new_x,new_y,new_color = prompt_user()
			if new_color is None:
				print("Exiting...")
				break
			
			# Update the colour/pixel
			current_color = new_color
			x = new_x
			y = new_y
			set_colour(x,y,current_color)

##################################################################################
		""" while True:
			#image = create_image((255,0,0),480,320)
			
			pixels1.fill((250,250,250))
			print('Drawing image')
			lcd.display(image)
			lcd1.display(image)
			time.sleep(1)
			pixels1.fill((0,0,0))
			time.sleep(1) """

	except KeyboardInterrupt:
        # catching keyboard interrupt to exit, but do the cleanup in finally block
		pass
	finally:
		GPIO.cleanup()
		spi.close()
		spi1.close()
