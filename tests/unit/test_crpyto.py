import pytest

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from shushi.crypto import _kdf, _salt, _key, _fernet


@pytest.fixture
def derived_key():
    yield (
        b'\x12bb\x04\xeb\xe2\xbc\xe4x\x9c\x83=\xda\xc4'
        b'\x13D\x00\xf4\xc9\xa0\x95\xe6\\0\xf44\xcc\x15\xa9\x83\xafb'
    )


@pytest.fixture
def key():
    yield b'EmJiBOvivOR4nIM92sQTRAD0yaCV5lww9DTMFamDr2I='


@pytest.fixture
def kdf(mocker, derived_key):
    obj = mocker.Mock(spec=PBKDF2HMAC)
    obj.derive.return_value = derived_key
    yield obj


def test_salt_returns_type():
    assert type(_salt()) == bytes


def test_salt_returns_length():
    assert len(_salt()) == 16


def test_kdf_returns_type(salt):
    assert type(_kdf(salt)) == PBKDF2HMAC


def test_key_returns_type(kdf, password):
    assert type(_key(kdf, password.encode())) == bytes


def test_fernet_returns_type(key):
    assert type(_fernet(key)) == Fernet
