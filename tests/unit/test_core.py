from shushi.core import _generate_salt


def test_generate_salt_returns_type(app_path):
    assert type(_generate_salt(app_path)) == bytes

# TODO: Add mocking to prevent live file creation.
