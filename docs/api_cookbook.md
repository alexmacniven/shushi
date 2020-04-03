# API Cookbook
The underlying API powering the CLI application is open for use.

Interacting with a shushi vault is via the commands `make`, `add`, `remove`, `list_names` and `get`.

This guide will demonstrate the usage of the commands. But first, you may want to check out the notes on (Environment Variables)[.\environment_variables.md].

## make
Creates a new vault in your `APPDATA`;
```pycon
>>> import shushi
>>> shushi.make("my_password")
```
***Passing the `force` flag as `True` will overwrite any existing vault in `APPDATA` without further warning.***
```pycon
>>> import shushi
>>> shushi.make("my_password", True)
```

## add
Adds a new item in the vault in your `APPDATA`;
```pycon
>>> import shushi
>>> new_item = dict(name="facebook", user="joe bloggs", password="secret_phrase")
>>> shushi.add(new_item, "my_password")
```
*A `KeyError` is raised when the item doesn't have a `name` key.*  
*An `ItemExists` error is raised when the vault already contains an item by the same name.*  
***Passing the `force` flag as `True` will overwrite the existing item in the vault with the supplied item.***  
```pycon
>>> import shushi
>>> new_item = dict(name="facebook", user="joe bloggs", password="secret_phrase")
>>> shushi.add(new_item, "my_password", True)
```

## remove
Removes an item from the vault in your `APPDATA`;
```pycon
>>> import shushi
>>> shushi.remove("facebook", "password")
```
*An `ItemNotFound` is raised when the vault contains no item by the supplied `name`.*

## list_names
Returns a list of all item names in the vault in your `APPDATA`;
```pycon
>>> import shushi
>>> shushi.list_names("password")
['twitter', 'facebook']
```

