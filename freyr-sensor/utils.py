__all__ = ["encode_params", "load_json", "save_json"]

import ujson


def encode_params(params: dict) -> str:
    encoded_params = []
    for key, value in params.items():
        encoded_params.append(str(key) + "=" + str(value))
    return "&".join(encoded_params)


def load_json(filename: str) -> dict:
    try:
        with open(filename) as stream:
            return ujson.load(stream)
    except OSError as err:
        print(f"Unable to load '{filename}':", err)
        return {}


def save_json(filename: str, data: dict) -> None:
    try:
        with open(filename, "w") as stream:
            ujson.dump(data, stream)
    except OSError as err:
        print(f"Unable to save '{filename}':", err)
