from shushi.record import VaultRecord


def test_vault_record_constructor():
    name = "twitter"
    data = dict(user="Joe", password="Bl0ggs")
    obj = VaultRecord(name, **data)
    assert obj.name == name
    assert obj.user == "Joe"
    assert obj.password == "Bl0ggs"
