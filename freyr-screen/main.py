import gc
from network import STA_IF, WLAN
from utime import sleep

from screen import Screen

from utils import load_json

wlan = WLAN(STA_IF)
# watchdog = WDT(timeout=8000)  # 8 Seconds  # noqa: ERA001


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
            # watchdog.feed()  # noqa: ERA001
            sleep(5)


config = load_json("config.json")
connect_to_wifi(ssid=config["wifi"]["ssid"], password=config["wifi"]["password"])
screen = Screen(base_url=config["freyr"]["base_url"])

while True:
    screen.update()

    print("Waiting 15min...")
    sleep_min(value=15)
