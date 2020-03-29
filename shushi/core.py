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
    # Pop name from item; raise exception when name not suppleied
    # Decrypt vault contents as data: raise exception when fail
    # When name in data keys and force is False: return False
    # Add key/val pair to data where key is name and val is item
    # Encrypt data as vault contents
    # Return True
    pass
