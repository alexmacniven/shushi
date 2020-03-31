import click
from . import core
from . import crypto
from typing import List
from .record import VaultRecord
from .constants import APPDATA


@click.group()
def cli():
    pass


@cli.command(help="Creates a new vault")
@click.argument("password")
@click.option(
    "--force",
    is_flag=True,
    flag_value=True,
    help="Forces creation even if a vault exists"
)
def make(password, force):
    vault_path = APPDATA.joinpath("vault")
    if not vault_path.is_file() or force:
        core.make_vault(APPDATA, password)
        click.echo("A new vault has been created\n")
    else:
        click.echo("Vault already exists. Run with --force to override\n")


@cli.command()
@click.argument("password")
@click.argument("name")
@click.option(
    "--force",
    is_flag=True,
    flag_value=True,
    help="Overwrites if an item exists with the same name"
)
def add(password, name, force):
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    decrypted: dict = crypto.decrypt(salt, password, vault)
    new_item: dict = item_builder(name)
    if core.add_item(new_item, decrypted, force):
        click.echo(f"Added new item: {name}")
        encrypted: bytes = crypto.encrypt(salt, password, decrypted)
        core.dump_vault(APPDATA, encrypted)
    else:
        click.echo("Item already exists. Run with --force to override\n\n")


def item_builder(name: str) -> dict:
    item_dict: dict = dict(name=name)
    count: int = 0
    while True:
        field: str = input(f"Field[{count}]: ")
        if field == "":
            break
        value: str = input(f"Value[{count}]: ")
        item_dict[field] = value
        count += 1
    return item_dict


@cli.command()
@click.argument("password")
@click.argument("name")
def get(password, name):
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    decrypted: dict = crypto.decrypt(salt, password, vault)
    item: VaultRecord = core.get_item(name, decrypted)
    if item is not None:
        for key, value in item.__dict__.items():
            click.echo(f"{key} -> {value}")
    else:
        click.echo(f"Item not matched: {name}")


@cli.command()
@click.argument("password")
@click.argument("name")
def remove(password, name):
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    decrypted: dict = crypto.decrypt(salt, password, vault)
    if core.remove_item(name, decrypted):
        click.echo(f"Item has been removed: {name}")
        encrypted: bytes = crypto.encrypt(salt, password, decrypted)
        core.dump_vault(APPDATA, encrypted)
    else:
        click.echo(f"Item not matched: {name}")


@cli.command()
@click.argument("password")
def list(password):
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    decrypted: dict = crypto.decrypt(salt, password, vault)
    items: List = core.list_items(decrypted)
    for item in items:
        click.echo(item)
