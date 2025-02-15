__all__ = ["get_current_date", "increment_date", "load_json"]

import ujson
import utime

import urequests


def load_json(filename: str) -> dict:
    try:
        with open(filename) as stream:
            return ujson.load(stream)
    except OSError as err:
        print(f"Unable to load '{filename}':", err)
        return {}


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
