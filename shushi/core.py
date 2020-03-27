from pathlib import Path

from .constants import APPDATA
from .crypto import _salt, encrypt


def make_vault(password):
    salt: bytes = _generate_salt(APPDATA)
    _build_vault(APPDATA, salt, password)


def _generate_salt(path: Path) -> bytes:
    salt: bytes = _salt()
    with path.joinpath("salt").open("wb") as binio:
        binio.write(salt)
    return salt


def _build_vault(path: Path, salt: bytes, password: str):
    enc_data: bytes = encrypt(salt, password, dict())
    with path.joinpath("vault").open("wb") as binio:
        binio.write(enc_data)
