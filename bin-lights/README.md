# Bin Lights

![Micropython](https://img.shields.io/badge/Micropython-1.23.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

Visually show what bins to put out each week.

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev 3x RGB LED Module](https://core-electronics.com.au/piicodev-3x-rgb-led-module.html)
- [PiicoDev Cables](https://core-electronics.com.au/piicodev/cables.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies: `mpremote mip install urequests`
4. Copy the src files to your device: `mpremote cp bin-lights/config.json bin-lights/bin_lights.py bin-lights/utils.py :`
5. Update the `config.json` file with your settings: `mpremote edit config.json`
6. Copy the main file device: `mpremote cp bin-lights/main.py :`
