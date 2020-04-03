import pytest  # noqa

from shushi.api import make, APPDATA


def test_make_vault_creates_file_path(password, mocker, tmp_path):
    mocker.patch("shushi.api.APPDATA", tmp_path)
    make(password)
    assert APPDATA.joinpath("vault").is_file()


def test_make_vault_creates_salt_path(password, mocker, tmp_path):
    mocker.patch("shushi.api.APPDATA", tmp_path)
    make(password)
    assert APPDATA.joinpath("salt").is_file()
