__all__ = ["TemperatureScreen"]

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_SSD1306 import WIDTH, create_PiicoDev_SSD1306

from clock import Clock


class TemperatureScreen:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock
        self._sensor = PiicoDev_BME280()
        self._display = create_PiicoDev_SSD1306()

    def display_readings(self, readings: tuple[float, float, float]) -> None:
        self._display.fill(0)

        self._display.text(self._clock.date_str(), 0, 0, 1)
        time_str = self._clock.time_str()
        self._display.text(time_str, (WIDTH - len(time_str) * 8) // 2, 9, 1)

        self._display.text(f"Temp: {readings[0]:0.2f}", 0, 27, 1)
        self._display.text(f"Humid: {readings[1]:0.2f}", 0, 36, 1)
        self._display.text(f"Press: {readings[2]:0.2f}", 0, 45, 1)

        self._display.show()

    def update(self) -> None:
        print("Starting update of TemperatureScreen")
        for module in (self._sensor, self._display):
            try:
                module.pwrLED(True)
            except AttributeError:
                pass

        temperature, pressure, humidity = self._sensor.values()
        self.display_readings(readings=(temperature, humidity, pressure))

        for module in (self._sensor, self._display):
            try:
                module.pwrLED(False)
            except AttributeError:
                pass
        print("Finished update of TemperatureScreen")
