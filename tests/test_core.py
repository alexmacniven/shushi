import pytest

from shushi.core import (VaultRecord, build_salt, build_vault,
                         add_item, get_item, list_items, remove_item,
                         _validate_item_name)
from shushi.exceptions import ItemExists, ItemNotFound


def test_build_salt_returns_type(tmp_path):
    assert type(build_salt(tmp_path)) == bytes


def test_build_vault_creates_file_path(tmp_path, salt, password):
    build_vault(tmp_path, salt, password)
    assert tmp_path.joinpath("vault").is_file()


def test_add_item_not_member_no_force(new_item, base_data, data_with_twit):
    add_item(new_item, base_data)
    assert base_data == data_with_twit


def test_add_item_is_member_no_force(new_item, data_with_twit):
    with pytest.raises(ItemExists):
        add_item(new_item, data_with_twit)


def test_add_item_is_member_with_force(new_item, data_with_twit):
    data = dict(
        twitter=dict(user="John", password="Sm1th"),
        reddit=dict(user="Tom", password="J0nes")
    )
    add_item(new_item, data, force=True)
    assert data == data_with_twit


def test_validate_item_name(new_item):
    assert _validate_item_name(new_item) == "twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_capitalized(new_item):
    new_item["name"] == "Twitter"
    assert _validate_item_name(new_item) == "twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_gaps(new_item):
    new_item["name"] = "the twitter"
    assert _validate_item_name(new_item) == "the_twitter"
    assert new_item == dict(user="Joe", password="Bl0ggs")


def test_validate_item_name_raises(new_item):
    new_item.pop("name")
    with pytest.raises(KeyError):
        _validate_item_name(new_item)


def test_remove_item_is_member(data_with_twit):
    name = "twitter"
    remove_item(name, data_with_twit)
    assert name not in data_with_twit.keys()


def test_remove_item_not_member(base_data):
    name = "facebook"
    with pytest.raises(ItemNotFound):
        remove_item(name, base_data)


def test_get_item_is_member(data_with_twit):
    record: VaultRecord = get_item("twitter", data_with_twit)
    assert record.name == "twitter"
    assert record.user == "Joe"
    assert record.password == "Bl0ggs"


def test_get_item_not_member(base_data):
    with pytest.raises(ItemNotFound):
        assert get_item("facebook", base_data)


def test_list_items(data_with_twit):
    assert list_items(data_with_twit) == ["twitter", "reddit"]
