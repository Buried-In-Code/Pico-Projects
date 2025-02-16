import gc
import ujson
from machine import RTC, WDT
from network import STA_IF, WLAN
from utime import sleep

import urequests

from bin_lights import BinLights
from temperature_screen import TemperatureScreen

wlan = WLAN(STA_IF)
rtc = RTC()
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


def set_time(timezone: str = None) -> None:
    try:
        if timezone:
            response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        else:
            response = urequests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
    except Exception as err:
        print(err)
        return
    datetime_str = data["datetime"].replace(data["utc_offset"], "")

    year, month, day = map(int, datetime_str[:10].split("-"))
    hour, minute, second = map(int, datetime_str[11:19].split(":"))
    rtc.datetime((year, month, day, data["day_of_week"], hour, minute, second, 0))


def sleep_min(value: int = 1) -> None:
    for _ in range(value):
        for _ in range(12):
            gc.collect()
            watchdog.feed()
            sleep(5)


config = load_json("config.json")
connect_to_wifi(ssid=config["wifi"]["ssid"], password=config["wifi"]["password"])
print(f"Before: {rtc.datetime()}")
set_time(timezone=config["timezone"])
print(f"After: {rtc.datetime()}")
temperature_screen = TemperatureScreen(rtc=rtc)
bin_lights = BinLights.from_config(rtc=rtc, config=config["bin-lights"])

watchdog.feed()

while True:
    bin_lights.update()

    for _ in range(60):
        temperature_screen.update()

        print("Waiting 1min...")
        sleep_min(value=1)
