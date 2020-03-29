from shushi.core import build_salt, build_vault, make_vault


def test_build_salt_returns_type(app_path):
    assert type(build_salt(app_path)) == bytes


def test_build_vault_creates_file_path(app_path, vault_path, salt, password):
    build_vault(app_path, salt, password)
    assert vault_path.is_file()


def test_make_vault_creates_file_path(password, vault_path, app_path):
    make_vault(app_path, password)
    assert vault_path.is_file()


def test_make_vault_creates_salt_path(password, salt_path, app_path):
    make_vault(app_path, password)
    assert salt_path.is_file()
