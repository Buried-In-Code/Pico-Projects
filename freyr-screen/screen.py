__all__ = ["Screen"]

from machine import Pin
from ucollections import deque

import urequests
from Pico_ePaper_2_9 import EPD_2in9_Landscape

from utils import datetime_to_str, encode_params, load_json, parse_timestamp, save_json


class ServiceError(Exception):
    pass


class Screen:
    BLACK: int = 0x00
    WHITE: int = 0xFF

    def __init__(self, base_url: str) -> None:
        self.pwrLED = Pin("LED", Pin.OUT)
        self.display = EPD_2in9_Landscape()
        self.base_url = base_url

        self.devices = deque((), 10)

        self.display_width = self.display.height
        self.display_height = self.display.width
        self.graph_width = (self.display_width - (42 * 2) - 10) // 2
        self.graph_height = self.display_height - 30

        devices = self.load_state()
        if devices:
            self.devices.extend(devices)

    @classmethod
    def load_state(cls) -> list:
        return load_json("state.json").get("devices", [])

    def save_state(self) -> None:
        return save_json("state.json", {"devices": list(self.devices)})

    def _get(self, endpoint: str, params: dict = None) -> list[dict]:
        if params is None:
            params = {}
        url = self.base_url + endpoint
        if params:
            url = f"{url}?{encode_params(params=params)}"
        response = urequests.get(url=url, headers=self.headers)
        if response.status_code != 200:
            raise ServiceError(f"Invalid response: {response.text}")
        return response.json()

    def load_devices(self) -> list[tuple[int, str]]:
        try:
            data = self._get(endpoint="/api/devices")
            return [(x.get("id"), x.get("name")) for x in data if x.get("id") and x.get("name")]
        except ServiceError as err:
            print(err)
            return []

    def load_device_readings(self, device_id: int) -> list[dict]:
        try:
            return self._get(
                endpoint=f"/api/devices/{device_id}/readings",
                params={"limit": min(self.graph_width, 100)},
            )
        except ServiceError as err:
            print(err)
            return []

    def graph(self, readings: list, key: str, offset: int = 0) -> None:
        text_start = offset + (self.graph_width + 42 - len(key) * 8) // 2, 20
        self.display.text(key, text_start[0], text_start[1], self.BLACK)

        max_value = max(
            [float(x[key.lower()]) for x in readings if x and x[key.lower()]], default=None
        )
        if max_value is None:
            return
        min_value = min([float(x[key.lower()]) for x in readings if x])
        scale = self.graph_height / (max_value - min_value)
        max_value_y = 30 + (self.graph_height - int((max_value - min_value) * scale))
        min_value_y = 30 + self.graph_height
        self.display.text(f"{max_value: 04.1f}", offset, max_value_y, self.BLACK)
        self.display.text(f"{min_value: 04.1f}", offset, min_value_y - 8, self.BLACK)

        for idx, reading in enumerate(reversed(readings)):
            value = float(reading[key.lower()])
            x = offset + 42 + idx
            y = 30 + (self.graph_height - int((value - min_value) * scale))
            self.display.pixel(x, y, 0)

    def update(self) -> None:
        print("Starting update of Freyr Screen")
        self.pwrLED.on()

        try:
            device_id, device_name = self.devices.pop()
        except IndexError:
            self.devices.extend(self.load_devices())
            try:
                device_id, device_name = self.devices.pop()
            except IndexError:
                device_id = -1

        readings = self.load_device_readings(device_id=device_id)
        self.display.Clear(self.WHITE)
        self.display.fill(self.WHITE)

        if not readings:
            invalid_text = "No Readings Available"
            center_x = (self.display_width - len(invalid_text) * 8) // 2
            center_y = (self.display_height - 8) // 2
            self.display.text(invalid_text, center_x, center_y, self.BLACK)
        else:
            date_text = datetime_to_str(
                datetime=parse_timestamp(timestamp=readings[1]["timestamp"])
            )
            date_start = (self.display_width - len(date_text) * 8) // 2, 1
            self.display.text(date_text, date_start[0], date_start[1], self.BLACK)

            device_start = (self.display_width - len(device_name) * 8) // 2, 10
            self.display.text(device_name, device_start[0], device_start[1], self.BLACK)

            self.display.vline(42 + 5 + self.graph_width, 20, self.display_height - 20, self.BLACK)

            self.graph(readings=readings, key="Temperature")
            self.graph(readings=readings, key="Humidity", offset=self.display_width // 2 + 5)

        self.display.display(self.display.buffer)

        self.pwrLED.off()
        print("Finished update of Freyr Screen")
