import pytest

from shushi.core import (VaultRecord, add_item, build_salt, build_vault,
                         get_item, list_items, make_vault, remove_item,
                         validate_item_name)


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


def test_add_item_not_member_no_force(new_item, populated_data):
    data = dict(reddit=dict(user="Tom", password="J0nes"))
    assert add_item(new_item, data) is True
    assert data == populated_data


def test_add_item_is_member_no_force(new_item, populated_data):
    data = populated_data
    assert add_item(new_item, data) is False
    assert data == populated_data


def test_add_item_is_member_with_force(new_item, populated_data):
    data = dict(
        twitter=dict(user="John", password="Sm1th"),
        reddit=dict(user="Tom", password="J0nes")
    )
    assert add_item(new_item, data, force=True) is True
    assert data == populated_data


def test_validate_item_name(new_item):
    assert validate_item_name(new_item) == "twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_capitalized(new_item):
    new_item["name"] == "Twitter"
    assert validate_item_name(new_item) == "twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_gaps(new_item):
    new_item["name"] = "the twitter"
    assert validate_item_name(new_item) == "the_twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_raises(new_item):
    new_item.pop("name")
    with pytest.raises(KeyError):
        validate_item_name(new_item)


def test_remove_item_is_member(populated_data):
    name = "twitter"
    assert remove_item(name, populated_data) is True
    assert name not in populated_data.keys()


def test_remove_item_not_member(populated_data):
    name = "facebook"
    assert remove_item(name, populated_data) is False
    assert "twitter" in populated_data.keys()
    assert "reddit" in populated_data.keys()


def test_get_item_is_member(populated_data):
    record: VaultRecord = get_item("twitter", populated_data)
    assert record.name == "twitter"
    assert record.user == "Joe"
    assert record.password == "Bl0ggs"


def test_get_item_not_member(populated_data):
    assert get_item("facebook", populated_data) is None


def test_list_items(populated_data):
    assert list_items(populated_data) == ["twitter", "reddit"]
