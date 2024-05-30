import ujson
from machine import Pin

import urequests
from waveshare_display import BLACK, WHITE, DisplayLandscape

from config import base_url


def parse_timestamp(timestamp: str) -> tuple[int, int, int, int, int, int]:
    parts = timestamp.split("T")
    year, month, day = map(int, parts[0].split("-"))
    hour, minute, second = map(int, parts[1].split(":"))
    return year, month, day, hour, minute, second


def datetime_to_str(datetime: tuple[int, int, int, int, int, int]) -> str:
    def zellers_congruence(year: int, month: int, day: int) -> int:
        if month < 3:
            month += 12
            year -= 1
        c = year // 100
        year = year % 100
        return (c // 4 - 2 * c + year + year // 4 + 13 * (month + 1) // 5 + day - 1) % 7

    weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "---"]
    weekday_name = weekdays[
        zellers_congruence(year=datetime[0], month=datetime[1], day=datetime[2])
    ]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_name = months[datetime[1] - 1]
    date_str = f"{weekday_name}, {datetime[2]:02d} {month_name} {datetime[0]:04d}"
    time_str = f"{datetime[3]:02d}:{datetime[4]:02d}:{datetime[5]:02d}"
    return f"{date_str} - {time_str}"


class FreyrSensor:
    def __init__(self) -> None:
        self.pwrLED = Pin("LED", Pin.OUT)
        self.display = DisplayLandscape()

        self.display_width = self.display.height
        self.display_height = self.display.width
        self.graph_width = (self.display_width - (42 * 2) - 10) // 2
        self.graph_height = self.display_height - 30

        self.last_device = self.load_state()

    @classmethod
    def load_state(cls) -> int:
        try:
            with open("freyr-screen_state.json") as stream:
                data = ujson.load(stream)
                return data["last_device"]
        except OSError as err:
            print("Error loading state:", err)
            return None

    def save_state(self) -> None:
        try:
            with open("freyr-screen_state.json", "w") as stream:
                ujson.dump({"last_device": self.last_device}, stream)
        except OSError as err:
            print("Error saving state:", err)

    def request_readings(self) -> tuple[str, list]:
        try:
            response = urequests.get(
                f"{base_url}/api/devices/{self.device_id}/readings?limit={self.graph_width}"
            )
            data = response.json()
            return data["name"], data["readings"]
        except Exception as err:  # noqa: BLE001
            print("Unable to get device readings:", err)
            return None, []

    def graph(self, readings: list, key: str, offset: int = 0) -> None:
        text_start = offset + (self.graph_width + 42 - len(key) * 8) // 2, 20
        self.display.text(key, text_start[0], text_start[1], BLACK)
        max_value = max([float(x[key.lower()]) for x in readings])
        min_value = min([float(x[key.lower()]) for x in readings])
        scale = self.graph_height / (max_value - min_value)
        max_value_y = 30 + (self.graph_height - int((max_value - min_value) * scale))
        min_value_y = 30 + self.graph_height
        self.display.text(f"{max_value: 04.1f}", offset, max_value_y, BLACK)
        self.display.text(f"{min_value: 04.1f}", offset, min_value_y - 8, BLACK)
        for idx, reading in enumerate(reversed(readings)):
            value = float(reading[key.lower()])
            x = offset + 42 + idx
            y = 30 + (self.graph_height - int((value - min_value) * scale))
            self.display.pixel(x, y, 0)

    def update(self) -> None:
        print("Starting update of Freyr Screen")
        self.pwrLED.on()

        device_name, readings = self.request_readings()
        self.display.clear(WHITE)
        self.display.fill(WHITE)

        if not device_name or not readings:
            invalid_text = "No Readings Available"
            center_x = (self.display_width - len(invalid_text) * 8) // 2
            center_y = (self.display_height - 8) // 2
            self.display.text(invalid_text, center_x, center_y, BLACK)
        else:
            date_text = datetime_to_str(
                datetime=parse_timestamp(timestamp=self.readings[1]["timestamp"])
            )
            date_start = (self.display_width - len(date_text) * 8) // 2, 1
            self.display.text(date_text, date_start[0], date_start[1], BLACK)

            device_start = (self.display_width - len(device_name) * 8) // 2, 10
            self.display.text(device_name, device_start[0], device_start[1], BLACK)

            self.display.vline(42 + 5 + self.graph_width, 20, self.display_height - 20, BLACK)

            self.graph(readings=readings, key="Temperature")
            self.graph(readings=readings, key="Humidity", offset=self.display_width // 2 + 5)

        self.display.display(self.display.buffer)
        self.display.delay_ms(2000)

        self.pwrLED.off()
        print("Finished update of Freyr Screen")
