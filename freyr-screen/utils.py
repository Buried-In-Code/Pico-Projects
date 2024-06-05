from utime import gmtime, time

from config import offset


def get_datetime(offset: int = offset) -> tuple[int, int, int, int, int, int, int, int]:
    return gmtime(time() + offset * 3600)


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
