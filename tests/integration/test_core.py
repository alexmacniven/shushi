from shushi.core import make_vault


def test_make_vault_creates_file_path(password, vault_path):
    make_vault(password)
    assert vault_path.is_file()


def test_make_vault_creates_salt_path(password, salt_path):
    make_vault(password)
    assert salt_path.is_file()

# TODO: Add mocking to prevent live file creation.
