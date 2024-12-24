__all__ = ["Bin", "BinLights"]

import urequests
from PiicoDev_RGB import PiicoDev_RGB

from utils import load_json, save_json


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


class BinLights:
    def __init__(
        self,
        active_days: list[int],
        bins: dict[str, Bin],
        bin_rotation: list[list[str]],
        timezone: str = None,
    ):
        self.active_days = active_days
        self.bins = bins
        self.bin_rotation = bin_rotation
        self.timezone = timezone
        self.last_updated, self.index = self.load_state()

    @staticmethod
    def from_config(config: dict, timezone: str = None):
        Bin.modules = [
            PiicoDev_RGB(bright=config["brightness"])
            for _ in range(max(x["module"] for x in config["bins"].values()) + 1)
        ]
        day_mapping = {
            "sunday": 0,
            "monday": 1,
            "tuesday": 2,
            "wednesday": 3,
            "thursday": 4,
            "friday": 5,
            "saturday": 6,
        }
        return BinLights(
            active_days=[day_mapping.get(x.casefold(), 7) for x in config["active_days"]],
            bins={k: Bin.from_config(config=v) for k, v in config["bins"]},
            bin_rotation=config["bin-rotation"],
            timezone=timezone,
        )

    @classmethod
    def load_state(cls) -> tuple[int, int]:
        data = load_json(filename="state.json")
        return data.get("last_updated"), data.get("index")

    def save_state(self) -> None:
        return save_json(
            filename="state.json", data={"last_updated": self.last_updated, "index": self.index}
        )

    def get_current_date(self) -> tuple[int, int]:
        try:
            if self.timezone:
                response = urequests.get(f"http://worldtimeapi.org/api/timezone/{self.timezone}")
            else:
                response = urequests.get("http://worldtimeapi.org/api/ip")
            data = response.json()
            return data.get("day_of_week"), data.get("week_number")
        except Exception as err:
            print("Error fetching current date:", err)
            return None, None

    def enable_lights(self, bins: list[str]) -> None:
        self.disable_lights()
        [self.bins[x].turn_on() for x in bins]

    def disable_lights(self) -> None:
        [x.turn_off() for x in self.bins]

    def update(self) -> None:
        print("Starting update of BinLights")
        for module in Bin.modules:
            module.pwrLED(True)

        day_of_week, week_number = self.get_current_date()
        if week_number is not None and week_number != self.last_updated:
            if self.last_updated is not None:
                self.index = 1 - self.index
            self.last_updated = week_number
            self.save_state()
        if day_of_week is not None:
            if day_of_week in self.active_days:
                self.enable_lights(bins=self.bin_rotation[self.index])
            else:
                self.disable_lights()

        for module in Bin.modules:
            module.pwrLED(False)
        print("Finished update of BinLights")
