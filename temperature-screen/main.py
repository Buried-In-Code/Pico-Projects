import gc
import ujson
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from clock import Clock
from temperature_screen import TemperatureScreen

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds


def load_json(filename: str) -> dict:
    try:
        with open(filename) as stream:
            return ujson.load(stream)
    except OSError as err:
        print(f"Unable to load '{filename}':", err)
        return {}


def connect_to_wifi(ssid: str, password: str) -> None:
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Waiting for connection...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f"Connected on {ip}")


def sleep_min(value: int = 1) -> None:
    for _ in range(value):
        for _ in range(12):
            gc.collect()
            watchdog.feed()
            sleep(5)


config = load_json("config.json")
connect_to_wifi(ssid=config["wifi"]["ssid"], password=config["wifi"]["password"])
clock = Clock(timezone=config["timezone"])
temperature_screen = TemperatureScreen(clock=clock)

while True:
    temperature_screen.update()

    print("Waiting 1min...")
    sleep_min(value=1)
