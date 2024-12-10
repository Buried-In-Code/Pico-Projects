__all__ = ["Sensor"]

from machine import Pin

import urequests
from dht import DHT22

from utils import encode_params, load_json, save_json


class ServiceError(Exception):
    pass


class Sensor:
    def __init__(self, pin: Pin, device_name: str, base_url: str) -> None:
        self.pwrLED = Pin("LED", Pin.OUT)
        self.sensor = DHT22(pin=pin)
        self.device_name = device_name
        self.headers = {
            "User-Agent": f"Freyr-Device/v2.1/{self.device_name}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.base_url = base_url

        self.device_id = self.load_state()
        if not self.device_id:
            self.device_id = self.check_device_exists()
            if not self.device_id:
                self.device_id = self.create_device()
                if not self.device_id:
                    raise ServiceError("Device not setup")
            self.save_state()

    @classmethod
    def load_state(cls) -> int:
        return load_json(filename="state.json").get("device_id")

    def save_state(self) -> None:
        return save_json(filename="state.json", data={"device": {"id": self.device_id}})

    def _get(
        self, endpoint: str, params: dict[str, str] = None, headers: dict[str, str] = None
    ) -> dict:
        if params is None:
            params = {}
        if headers is None:
            headers = self.headers
        url = self.base_url + endpoint
        if params:
            url = f"{url}?{encode_params(params=params)}"
        response = urequests.get(url=url, headers=headers)
        if response.status_code != 200:
            raise ServiceError(f"Invalid response: {response.text}")
        return response.json()

    def _post(
        self,
        endpoint: str,
        params: dict[str, str] = None,
        headers: dict[str, str] = None,
        body: dict = None,
    ) -> dict:
        if params is None:
            params = {}
        if headers is None:
            headers = self.headers
        if body is None:
            body = {}
        url = self.base_url + endpoint
        if params:
            url = f"{url}?{encode_params(params=params)}"
        response = urequests.post(url=url, headers=headers, json=body)
        if response.status_code not in (200, 201):
            raise ServiceError(f"Invalid response: {response.text}")
        return response.json()

    def check_device_exists(self) -> int:
        try:
            data = self._get(endpoint="/api/devices", params={"name": self.device_name, "limit": 1})
            if not data:
                return None
            return data[0].get("id")
        except ServiceError as err:
            print(err)
            return None

    def create_device(self) -> int:
        data = self._post(endpoint="/api/devices", body={"name": self.device_name})
        return data.get("id")

    def update(self) -> None:
        print("Starting update of Sensor")
        self.pwrLED.on()

        self.sensor.measure()
        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()
        self._post(
            endpoint=f"/api/devices/{self.device_id}/readings",
            body={"temperature": temperature, "humidity": humidity},
        )

        self.pwrLED.off()
        print("Finished update of Sensor")
