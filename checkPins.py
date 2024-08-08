import RPi.GPIO as GPIO

# Set the pin numbering mode to BOARD
GPIO.setmode(GPIO.BOARD)

# List of all physical pins on the Raspberry Pi (BOARD numbering)
board_pins = list(range(1, 41))  # Adjust the range if needed

# Initialize pin configurations
pin_configs = {}

# Function to check pin configuration
def check_pin_config(pin):
    try:
        GPIO.setup(pin, GPIO.OUT)  # Try to set pin as output
        pin_configs[pin] = "Output"
    except RuntimeError:
        try:
            GPIO.setup(pin, GPIO.IN)  # Try to set pin as input
            pin_configs[pin] = "Input"
        except RuntimeError:
            pin_configs[pin] = "Unconfigured or Error"

# Check configuration of each pin
for pin in board_pins:
    check_pin_config(pin)

# Print the configuration of each pin
for pin, config in pin_configs.items():
    print(f"Pin {pin}: {config}")

# Clean up GPIO settings
GPIO.cleanup()
