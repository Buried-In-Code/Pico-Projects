mpremote mip install urequests
mkdir lib
wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py -O lib/PiicoDev_Unified.py
wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-BME280-MicroPython-Module/main/PiicoDev_BME280.py -O lib/PiicoDev_BME280.py
wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-SSD1306-MicroPython-Module/main/PiicoDev_SSD1306.py -O lib/PiicoDev_SSD1306.py
mpremote cp -r lib/ :
mpremote cp temperature_screen.py config.json main.py :
mpremote edit config.json
