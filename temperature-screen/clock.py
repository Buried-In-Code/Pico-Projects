__all__ = ["Clock"]

import utime

import urequests


class Clock:
    def __init__(self, timezone: str = None) -> None:
        try:
            if timezone:
                response = urequests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
            else:
                response = urequests.get("http://worldtimeapi.org/api/ip")
            data = response.json()
            datetime_str = data["datetime"]
            utc_offset = data["utc_offset"]

            year, month, day = map(int, datetime_str[:10].split("-"))
            hour, minute, second = map(int, datetime_str[11:19].split(":"))
            self.offset = int(utc_offset.replace(":", "."))

            unix_time = utime.mktime((year, month, day, hour, minute, second, 0, 0))
            local_time = unix_time + self.offset * 3600
            utime.localtime(local_time)

            utime.time()
        except Exception as err:
            print(err)

    def get_datetime(self) -> tuple[int, int, int, int, int, int, int, int]:
        return utime.gmtime(utime.time() + self.offset * 3600)

    def date_str(self) -> str:
        year, month, day, _, _, _, day_of_week, _ = self.get_datetime()
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
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
        _, _, _, hour, minute, second, _, _ = self.get_datetime()
        return f"{hour:02d}:{minute:02d}:{second:02d}"
