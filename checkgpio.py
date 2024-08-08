import RPi.GPIO as GPIO

# Set the pin numbering mode
GPIO.setmode(GPIO.BCM)

# List of all BCM pins for Raspberry Pi
bcm_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]

# Function to get pin configuration
def get_pin_config(pin):
    try:
        mode = GPIO.gpio_function(pin)
        if mode == GPIO.OUT:
            return "Output"
        elif mode == GPIO.IN:
            return "Input"
        elif mode == GPIO.SPI:
            return "SPI"
        elif mode == GPIO.I2C:
            return "I2C"
        elif mode == GPIO.SERIAL:
            return "Serial"
        elif mode == GPIO.HARD_PWM:
            return "Hardware PWM"
        elif mode == GPIO.UNKNOWN:
            return "Unknown"
    except RuntimeError as e:
        return f"Error: {e}"

# Print the configuration of each pin
for pin in bcm_pins:
    config = get_pin_config(pin)
    print(f"Pin {pin}: {config}")

# Clean up GPIO settings
GPIO.cleanup()
