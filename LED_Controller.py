import RPi.GPIO as GPIO
import numpy as np
import threading
import board
import neopixel
from dataclasses import dataclass

@dataclass
class Board_Config:
    board_pin: board.Pin
    board_n: int
    brightness: int

class LED_Controller:
	def __init__(self, pixels = neopixel.NeoPixel(board.D18, 64, brightness = 1), board_config:Board_Config = None, grid_size:int = 8):
		if board_config != None:
			self.pixels = pixels
		self.thread = None
		self.grid_size = grid_size

	def set_colour(self, x:int = 1, y:int = 1, rgb_tuple:tuple[int,int,int] = (255,0,0)):
		self.pixels[x+y*self.grid_size]
		self.pixels.show()
  
	def fill_individual_pixel(self, color_array:np.array):
		assert len(color_array) == self.grid_size ** 2 or color_array.shape == (self.grid_size, self.grid_size), "The color_array should be either a matrix of {self.grid_size} x {self.grid_size} or an array of size {self.grid_size ** 2}"
		for i in range(self.grid_size):
			for j in range(self.grid_size):
				self.set_colour(i, j, color_array[i][j])
		self.pixels.show()

	def prompt_user():
		# Prompt user until valid input is given
		while True:
			try:
				# Get RGB input and split by commas
				RGB_input = input("Enter RGB values (e.g., 255,0,0): ")
				new_x = int(input("Pixel (x): "))
				new_y = int(input("Pixel (y): "))

				# Convert RGB values to integers and strip any extra spaces
				rgb_values = RGB_input.split(',')
				rgb_tuple = tuple(int(value.strip()) for value in rgb_values)

				# Validate that exactly 3 RGB values are provided
				if len(rgb_tuple) != 3:
					raise ValueError("Enter exactly three values separated by commas.")
				
				# Validate that x and y are non-negative integers
				if new_x < 0 or new_y < 0:
					raise ValueError("Pixel coordinates (x, y) must be non-negative integers.")
				
				# Return the pixel coordinates and RGB tuple
				return new_x, new_y, rgb_tuple
			
			except ValueError as e:
				# Print the error and prompt the user again
				print(f"Invalid input: {e}")
    
	def start_prompt_user_thread(self):
		self.thread = threading.Thread(target=self.prompt_user)
		self.thread.start()
	
	def clear_board(self):
		self.pixels.fill((0,0,0))
		self.pixels.show()
	
	def close(self):
		self.pixels.fill((0,0,0))
		self.pixels.show()
		if self.thread != None:
			self.thread.join()
  
if __name__ == '__main__':
	try:
		board_config = Board_Config(board_pin = board.D18, board_n = 64, brightness = 1)
		lcd_controller = LED_Controller(board_config=board_config)
		print("Starting thread to control the pixels on the board")
		lcd_controller.start_prompt_user_thread()
	except KeyboardInterrupt:
        # catching keyboard interrupt to exit, but do the cleanup in finally block
		pass
	finally:
		lcd_controller.clear_board()
		lcd_controller.close()
		GPIO.cleanup()
