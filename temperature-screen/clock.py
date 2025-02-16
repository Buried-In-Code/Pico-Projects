__all__ = ["Clock"]

import urequests


class Clock:
    def __init__(self, timezone: str = None) -> None:
        self.timezone = timezone

    def get_datetime(self) -> tuple[int, int, int, int, int, int, int]:
        try:
            if self.timezone:
                response = urequests.get(f"http://worldtimeapi.org/api/timezone/{self.timezone}")
            else:
                response = urequests.get("http://worldtimeapi.org/api/ip")
            data = response.json()
        except Exception as err:
            print(err)
        datetime_str = data["datetime"].replace(data["utc_offset"], "")

        year, month, day = map(int, datetime_str[:10].split("-"))
        hour, minute, second = map(int, datetime_str[11:19].split(":"))
        return year, month, day, hour, minute, second, data["day_of_week"]

    def date_str(self) -> str:
        year, month, day, _, _, _, day_of_week = self.get_datetime()
        weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        weekday_name = weekdays[day_of_week]
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        month_name = months[month - 1]
        return f"{weekday_name}, {day:02d} {month_name} {year:04d}"

    def time_str(self) -> str:
        _, _, _, hour, minute, second, _ = self.get_datetime()
        return f"{hour:02d}:{minute:02d}:{second:02d}"
