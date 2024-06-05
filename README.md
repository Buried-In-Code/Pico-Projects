# Pico Projects

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

## Projects

### FreyrSensor

Collects temperature and humidity readings and sends them to Freyr.

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [DHT22 sensor](https://core-electronics.com.au/dht22-module-temperature-and-humidity.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies: `mpremote mip install dht urequests`
4. Copy the src files to your device: `mpremote cp freyr-sensor/config.py freyr-sensor/freyr_sensor.py freyr-sensor/utils.py :`
5. Update the `config.py` file with your settings: `mpremote edit config.py`
6. Copy the main file device: `mpremote cp freyr-sensor/main.py :`

### FreyrScreen

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [Waveshare 2.9inch E-Paper](https://core-electronics.com.au/waveshare-2-9inch-e-paper-module-for-raspberry-pi-pico-296x128-black-white.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies: `mpremote mip install urequests`
4. Create a lib folder: `mkdir lib`
5. Download the Waveshare library: `wget https://raw.githubusercontent.com/waveshareteam/Pico_ePaper_Code/main/python/Pico_ePaper-2.9.py -O lib/Pico_ePaper_2_9.py`
6. Copy the libraries to your device: `mpremote cp -r lib/ :`
7. Copy the src files to your device: `mpremote cp freyr-screen/config.py freyr-screen/freyr_screen.py freyr-screen/utils.py :`
8. Update the `config.py` file with your settings: `mpremote edit config.py`
9. Copy the main file device: `mpremote cp freyr-screen/main.py :`
