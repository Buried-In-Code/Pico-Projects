__all__ = ["TemperatureScreen"]

from machine import RTC

from PiicoDev_BME280 import PiicoDev_BME280
from PiicoDev_SSD1306 import WIDTH, create_PiicoDev_SSD1306


def date_format(rtc: RTC) -> str:
    year, month, day, day_of_week, _, _, _, _ = rtc.datetime()
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekday_name = weekdays[day_of_week]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    month_name = months[month - 1]
    return f"{weekday_name}, {day:02d} {month_name} {year:04d}"


def time_format(rtc: RTC) -> str:
    _, _, _, _, hour, minute, second, _ = rtc.datetime()
    return f"{hour:02d}:{minute:02d}:{second:02d}"


class TemperatureScreen:
    def __init__(self, rtc: RTC) -> None:
        self._rtc = rtc
        self._sensor = PiicoDev_BME280()
        self._display = create_PiicoDev_SSD1306()

    def display_readings(self, readings: tuple[float, float, float]) -> None:
        self._display.fill(0)

        date_str = date_format(self._rtc)
        self._display.text(date_str, (WIDTH - len(date_str) * 8) // 2, 0, 1)
        time_str = time_format(self._rtc)
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
        pressure = pressure / 100
        self.display_readings(readings=(temperature, humidity, pressure))

        for module in (self._sensor, self._display):
            try:
                module.pwrLED(False)
            except AttributeError:
                pass
        print("Finished update of TemperatureScreen")
