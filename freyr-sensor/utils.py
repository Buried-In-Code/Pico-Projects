from utime import gmtime, time

from config import offset


def get_datetime(offset: int = offset) -> tuple[int, int, int, int, int, int, int, int]:
    return gmtime(time() + offset * 3600)
