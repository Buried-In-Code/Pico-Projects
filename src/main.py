import gc
import ntptime
from machine import WDT
from network import STA_IF, WLAN
from utime import sleep

from config import password, ssid

wlan = WLAN(STA_IF)
watchdog = WDT(timeout=8000)  # 8 Seconds

try:
    from freyr_sensor import FreyrSensor

    freyr_sensor = FreyrSensor()
except ImportError:
    freyr_sensor = None


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


def main() -> None:
    connect_to_wifi()
    set_time()

    print(f"FreyrSensor enabled: {freyr_sensor is not None}")
    if not freyr_sensor:
        return

    while True:
        if freyr_sensor:
            freyr_sensor.update()

        print("Waiting 5min...")
        sleep_min(value=5)


main()
