#include all necessary packages to get LEDs to work with Raspberry Pi
import time
import board
import neopixel

#Initialise a strips variable, provide the GPIO Data Pin
#utilised and the amount of LED Nodes on strip and brightness (0 to 1 value)
pixels1 = neopixel.NeoPixel(board.D18, 64, brightness=1)

#Also create an arbitrary count variable
x=0

#Focusing on a particular strip, use the command Fill to make it all a single colour
#based on decimal code R, G, B. Number can be anything from 255 - 0. Use an RGB Colour
#Code Chart Website to quickly identify the desired fill colour.
#pixels1.fill((30, 0, 0))
# time.sleep(4)
# pixels1.fill((0, 30, 0))
# time.sleep(4)
# pixels1.fill((0, 0, 30))
# time.sleep(4)
pixels1.fill((250,250,250))
# time.sleep(5)
pixels1.fill((0,0,0,0))
# time.sleep(1)