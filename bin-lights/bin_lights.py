__all__ = ["BinLights"]

import utime

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


def get_current_date(timezone: str = None) -> str:
    try:
        if timezone:
            response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        else:
            response = urequests.get("http://worldtimeapi.org/api/ip")
        data = response.json()
        return data.get("datetime").split("T")[0]
    except Exception as err:
        print("Error fetching current date:", err)
        return None


def increment_date(date_str: str) -> str:
    year, month, day = map(int, date_str.split("-"))
    time_tuple = (year, month, day, 0, 0, 0, 0, 0, -1)
    timestamp = utime.mktime(time_tuple)
    timestamp += 86400
    new_time_tuple = utime.localtime(timestamp)
    return f"{new_time_tuple[0]:04d}-{new_time_tuple[1]:02d}-{new_time_tuple[2]:02d}"


class BinLights:
    def __init__(self, bins: dict[str, Bin], data_url: str, timezone: str = None):
        self.bins = bins
        self.data_url = data_url
        self.timezone = timezone

    @staticmethod
    def from_config(config: dict, timezone: str = None):
        Bin.modules = [
            PiicoDev_RGB(bright=config["brightness"])
            for _ in range(max(x["module"] for x in config["bins"].values()) + 1)
        ]
        return BinLights(
            bins={k: Bin.from_config(config=v) for k, v in config["bins"]},
            data_url=config["data-url"],
            timezone=timezone,
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
        [x.turn_off() for x in self.bins]

    def update(self) -> None:
        print("Starting update of BinLights")
        for module in Bin.modules:
            module.pwrLED(True)

        bin_data = self.download_bin_data()
        today_str = get_current_date(timezone=self.timezone)
        tomorrow_str = increment_date(date_str=today_str)

        if today_str in bin_data:
            self.enable_lights(bins=bin_data[today_str])
        elif tomorrow_str in bin_data:
            self.enable_lights(bins=bin_data[tomorrow_str])
        else:
            self.disable_lights()

        for module in Bin.modules:
            module.pwrLED(False)
        print("Finished update of BinLights")
