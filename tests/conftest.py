import pytest


@pytest.fixture
def salt():
    return b'\xbc\xcd\xd7#\xf1N\xfc>(\xf30\xc2\xb9\xac\x0c\xd3'


@pytest.fixture
def password():
    return "my_password"


@pytest.fixture
def dec_data():
    return dict(age=23, first_name="Joe", last_name="Bloggs")


@pytest.fixture
def enc_data():
    return (
        b'gAAAAABefNCRCBGG0iOguedlXqgGA9Y4DMoBJdYCgz1ztqlL1_60X6NRfNHEPnDWkBkl'
        b'cneygudegEb_RHXERH8ktOP4pFkwfGbmzqWE9ikGGcRGZQFME9tHjESSZ0BqNR3DOXsV'
        b'477A-fXyHQdWCjCPqyxwowf70Q=='
    )
