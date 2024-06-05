import ujson
from machine import Pin

import urequests
from dht import DHT22

from config import base_url, device_name, sensor_pin
from utils import encode_params, get_datetime

headers = {
    "User-Agent": f"Freyr-Device/v2.0/{device_name}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


class FreyrSensor:
    def __init__(self) -> None:
        self.pwrLED = Pin("LED", Pin.OUT)
        self.sensor = DHT22(pin=Pin(sensor_pin))

        self.device_id = self.load_state()

    @classmethod
    def load_state(cls) -> int:
        try:
            with open("state.json") as stream:
                data = ujson.load(stream)
                return data["device_id"]
        except OSError as err:
            print("Error loading state:", err)
            return None

    def save_state(self) -> None:
        try:
            with open("state.json", "w") as stream:
                ujson.dump({"device_id": self.device_id}, stream)
        except OSError as err:
            print("Error saving state:", err)

    def check_device_exists(self) -> int:
        response = urequests.get(
            url=f"{base_url}/api/devices?{encode_params(params={"name": device_name, "limit": 1})}",
            headers=headers,
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if not data:
            return None
        return data[0]["id"]

    def create_device(self) -> int:
        body = {"name": device_name}
        response = urequests.post(url=f"{base_url}/api/devices", json=body, headers=headers)
        if response.status_code != 201:
            raise OSError(f"Failed to connect: {response.text}")
        data = response.json()
        return data["id"]

    def send_measurement(
        self, datetime: str, temperature: float = None, humidity: float = None
    ) -> None:
        body = {"timestamp": datetime, "temperature": temperature, "humidity": humidity}
        response = urequests.post(
            url=f"{base_url}/api/devices/{self.device_id}/readings", json=body, headers=headers
        )
        if response.status_code != 201:
            raise OSError(f"Failed to connect: {response.text}")

    def update(self) -> None:
        print("Starting update of Freyr Sensor")
        self.pwrLED.on()

        if not self.device_id:
            self.device_id = self.check_device_exists()
            if not self.device_id:
                self.device_id = self.create_device()

        self.sensor.measure()
        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()
        year, month, day, hour, minute, second, _, _ = get_datetime()
        datetime = f"{year:04d}-{month:02d}-{day:02d}T{hour:02d}:{minute:02d}:{second:02d}"
        self.send_measurement(datetime=datetime, temperature=temperature, humidity=humidity)

        self.save_state()

        self.pwrLED.off()
        print("Finished update of Freyr Sensor")
