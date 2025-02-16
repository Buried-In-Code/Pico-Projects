__all__ = ["BinLights"]

import utime
from machine import RTC

import urequests
from PiicoDev_RGB import PiicoDev_RGB


class Bin:
    modules = []

    def __init__(self, module: int, led: int, colour: tuple[int, int, int]):
        self._module = module
        self._led = led
        self._colour = colour

    @staticmethod
    def from_config(config: dict):
        return Bin(module=config["module"], led=config["led"], colour=config["colour"])

    def turn_on(self) -> None:
        self.modules[self._module].setPixel(self._led, self.colour)
        self.modules[self._module].show()

    def turn_off(self) -> None:
        self.modules[self._module].setPixel(self._led, [0, 0, 0])
        self.modules[self._module].show()


def get_tomorrow_date(rtc: RTC) -> str:
    year, month, day, _, _, _, _, _ = rtc.datetime()

    timestamp = utime.mktime((year, month, day, 0, 0, 0, 0, 0, -1)) + 86400
    tomorrow_tuple = utime.localtime(timestamp)

    return f"{tomorrow_tuple[0]:04d}-{tomorrow_tuple[1]:02d}-{tomorrow_tuple[2]:02d}"


class BinLights:
    def __init__(self, bins: dict[str, Bin], data_url: str, rtc: RTC):
        self.bins = bins
        self.data_url = data_url
        self._rtc = rtc

    @staticmethod
    def from_config(config: dict, rtc: RTC):
        Bin.modules = [
            PiicoDev_RGB(bright=config["brightness"])
            for _ in range(max(x["module"] for x in config["bins"].values()) + 1)
        ]
        return BinLights(
            bins={k: Bin.from_config(config=v) for k, v in config["bins"].items()},
            data_url=config["data-url"],
            rtc=rtc,
        )

    def download_bin_data(self) -> dict[str, list[str]]:
        try:
            response = urequests.get(self.data_url)
            return response.json()
        except Exception as err:
            print("Error fetching bin data:", err)
            return {}

    def enable_lights(self, bins: list[str]) -> None:
        self.disable_lights()
        [self.bins[x].turn_on() for x in bins]

    def disable_lights(self) -> None:
        [v.turn_off() for _, v in self.bins.items()]

    def update(self) -> None:
        print("Starting update of BinLights")
        for module in Bin.modules:
            module.pwrLED(True)

        bin_data = self.download_bin_data()
        today = self._rtc.datetime()
        today_str = f"{today[0]:04d}-{today[1]:02d}-{today[2]:02d}"
        tomorrow_str = get_tomorrow_date(rtc=self._rtc)

        if today_str in bin_data:
            self.enable_lights(bins=bin_data[today_str])
        elif tomorrow_str in bin_data:
            self.enable_lights(bins=bin_data[tomorrow_str])
        else:
            self.disable_lights()

        for module in Bin.modules:
            module.pwrLED(False)
        print("Finished update of BinLights")
