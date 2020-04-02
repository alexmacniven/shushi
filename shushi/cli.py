import os
from typing import List

import click

from . import core, crypto
from .constants import APPDATA
from .data import SetupFacts
from .exceptions import (IncorrectPassword, ItemExists, ItemNotFound,
                         VaultExists)
from .record import VaultRecord


@click.group()
@click.option("-p", "--password", default=None, help="Vault password")
@click.pass_context
def cli(ctx, password):
    ctx.ensure_object(dict)
    # Supplied password overrides environment password.
    ctx.obj["password"] = password or os.environ.get("SHUSHI_PASSWORD", None)
    if not ctx.obj.get("password"):
        click.echo("Error: A password has not been supplied.")
        ctx.abort()


@cli.command(help="Creates a new vault")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    flag_value=True,
    help="Forces creation even if a vault exists"
)
@click.pass_context
def make(ctx, force):
    try:
        core.make(ctx.obj.get("password"), force)
    except VaultExists as exc:
        exc.show()
        raise SystemExit(exc.exit_code)
    click.echo(f"Done: Vault has been created at [{APPDATA}]")


@cli.command(help="Adds a new item")
@click.argument("name")
@click.option(
    "--force",
    is_flag=True,
    flag_value=True,
    help="Overwrites if an item exists with the same name"
)
@click.pass_context
def add(ctx, name, force):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))
    new_item: dict = item_builder(name)

    try:
        core.add_item(new_item, artifacts.decrypted, force)
    except ItemExists as exc:
        exc.show()
        raise SystemExit(exc.exit_code)

    click.echo(f"Done: A new item [{name}] has been added.")
    encrypted: bytes = crypto.encrypt(
        artifacts.salt,
        ctx.obj.get("password"),
        artifacts.decrypted
    )
    core.dump_vault(APPDATA, encrypted)


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


@cli.command(help="Returns an item")
@click.argument("name")
@click.pass_context
def get(ctx, name):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))

    try:
        item: VaultRecord = core.get_item(name, artifacts.decrypted)
    except ItemNotFound as exc:
        exc.show()
        raise SystemExit(exc.exit_code)

    for key, value in item.__dict__.items():
        click.echo(f"[{key}]:: ", nl=False)
        click.echo(f"{value}")


@cli.command(help="Removes an item")
@click.argument("name")
@click.pass_context
def remove(ctx, name):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))
    try:
        core.remove_item(name, artifacts.decrypted)
    except ItemNotFound as exc:
        exc.show()
        raise SystemExit(exc.exit_code)

    click.echo(f"Done: An item [{name}] has been removed.")
    encrypted: bytes = crypto.encrypt(
        artifacts.salt,
        ctx.obj.get("password"),
        artifacts.decrypted,
    )
    core.dump_vault(APPDATA, encrypted)


@cli.command(help="Returns all item names")
@click.pass_context
def list(ctx):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))
    items: List = core.list_items(artifacts.decrypted)
    for item in items:
        click.echo(item)


def setup(password) -> SetupFacts:
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    try:
        decrypted: dict = crypto.decrypt(salt, password, vault)
    except IncorrectPassword as exc:
        exc.show()
        raise SystemExit(exc.exit_code)
    return SetupFacts(salt, vault, decrypted)
