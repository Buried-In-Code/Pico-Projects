# Freyr Screen

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

Pulls temperature and humidity readings from [Freyr](https://github.com/Buried-In-Code/Freyr) and displays results in graphs.

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
7. Copy the src files to your device: `mpremote cp freyr-screen/config.json freyr-screen/screen.py freyr-screen/utils.py :`
8. Update the `config.json` file with your settings: `mpremote edit config.json`
9. Copy the main file device: `mpremote cp freyr-screen/main.py :`
