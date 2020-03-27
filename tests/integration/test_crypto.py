from shushi.crypto import make_fernet, encrypt, decrypt, Fernet


def test_make_fernet_returns_type(salt, password):
    assert type(make_fernet(salt, password)) == Fernet


def test_encrypt_returns_type(salt, password, dec_data):
    assert type(encrypt(salt, password, dec_data)) == bytes


def test_decrypt_returns_value(salt, password, enc_data, dec_data):
    assert decrypt(salt, password, enc_data) == dec_data
