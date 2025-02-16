mpremote mip install urequests
mkdir lib
wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-Unified/main/PiicoDev_Unified.py -O lib/PiicoDev_Unified.py
wget https://raw.githubusercontent.com/CoreElectronics/CE-PiicoDev-RGB-LED-MicroPython-Module/main/PiicoDev_RGB.py -O lib/PiicoDev_RGB.py
mpremote cp -r lib/ :
mpremote cp bin_lights.py config.json main.py :
mpremote edit config.json
