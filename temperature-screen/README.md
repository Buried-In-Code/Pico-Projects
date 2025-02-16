# Temperature Screen

![Micropython](https://img.shields.io/badge/Micropython-1.24.1-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-informational?logo=pre-commit&style=flat-square)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/badge/ruff-enabled-informational?logo=ruff&style=flat-square)](https://github.com/astral-sh/ruff)

Record the temperature, humidity and pressure, and then display it on a screen.

#### Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [PiicoDev Cables](https://core-electronics.com.au/piicodev/cables.html)
- [PiicoDev OLED Display Module](https://core-electronics.com.au/piicodev-oled-display-module-128x64-ssd1306.html)
- [PiicoDev Precision Temperature Sensor Module](https://core-electronics.com.au/piicodev-precision-temperature-sensor-tmp117.html)

#### Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Run the installer: `./install.sh`
