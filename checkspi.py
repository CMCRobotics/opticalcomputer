import spidev

def list_spi_devices():
    spi_devices = []
    for bus in range(2):  # Typically, SPI buses 0 and 1 are used
        for device in range(2):  # Usually, devices are addressed as 0 and 1
            try:
                spi = spidev.SpiDev()
                spi.open(bus, device)
                spi.max_speed_hz = 50000
                spi.lsbfirst = False
                spi.mode = 0b00
                spi.close()
                spi_devices.append((bus, device))
            except IOError:
                pass  # Skip devices that cannot be opened
    return spi_devices

if __name__ == "__main__":
    devices = list_spi_devices()
    for bus, device in devices:
        print(f"SPI device found on bus {bus}, device {device}")
