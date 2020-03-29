from pathlib import Path

from .crypto import _salt, encrypt


def make_vault(path: Path, password: str):
    salt: bytes = build_salt(path)
    build_vault(path, salt, password)


def build_salt(path: Path) -> bytes:
    salt: bytes = _salt()
    with path.joinpath("salt").open("wb") as binio:
        binio.write(salt)
    return salt


def build_vault(path: Path, salt: bytes, password: str):
    enc_data: bytes = encrypt(salt, password, dict())
    with path.joinpath("vault").open("wb") as binio:
        binio.write(enc_data)


def add_item(item: dict, data: dict, force: bool = False) -> bool:
    item_name = validate_item_name(item)
    if item_name in data.keys() and not force:
        return False
    data[item_name] = item
    return True


def validate_item_name(item: dict) -> str:
    raw_name: str = item.pop("name")  # raises KeyError
    small_name: str = raw_name.lower()
    snake_name: str = small_name.replace(" ", "_")
    return snake_name
