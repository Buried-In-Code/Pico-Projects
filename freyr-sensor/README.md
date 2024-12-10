# Freyr Sensor

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

Collects temperature and humidity readings and sends them to [Freyr](https://github.com/Buried-In-Code/Freyr).

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [DHT22 sensor](https://core-electronics.com.au/dht22-module-temperature-and-humidity.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies: `mpremote mip install dht urequests`
4. Copy the src files to your device: `mpremote cp freyr-sensor/config.json freyr-sensor/sensor.py freyr-sensor/utils.py :`
5. Update the `config.json` file with your settings: `mpremote edit config.json`
6. Copy the main file device: `mpremote cp freyr-sensor/main.py :`
