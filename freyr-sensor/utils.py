from utime import gmtime, time

from config import offset


def get_datetime(offset: int = offset) -> tuple[int, int, int, int, int, int, int, int]:
    return gmtime(time() + offset * 3600)


def encode_params(params: dict) -> str:
    encoded_params = []
    for key, value in params.items():
        encoded_params.append(str(key) + "=" + str(value))
    return "&".join(encoded_params)
