import gc
import ntptime
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from config import password, ssid
from freyr_screen import FreyrScreen

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def connect_to_wifi() -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


def set_time() -> None:
    while True:
        try:
            ntptime.settime()
            return
        except OSError as err:
            print("Failed to set time:", err)


def sleep_min(value: int = 1) -> None:
    for _ in range(value):
        for _ in range(12):
            gc.collect()
            watchdog.feed()
            sleep(5)


connect_to_wifi()
set_time()
freyr_screen = FreyrScreen()

while True:
    freyr_screen.update()

    print("Waiting 15min...")
    sleep_min(value=15)
