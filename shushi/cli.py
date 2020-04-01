import os
from typing import List

import click

from . import core, crypto
from .data import SetupFacts
from .exceptions import IncorrectPassword
from .constants import APPDATA
from .record import VaultRecord


@click.group()
@click.option("-p", "--password", default=None, help="Vault password")
@click.pass_context
def cli(ctx, password):
    ctx.ensure_object(dict)
    # Supplied password overrides environment password.
    ctx.obj["password"] = password or os.environ.get("SHUSHI_PASSWORD", None)
    if not ctx.obj.get("password"):
        click.secho("A password has not been supplied", fg="bright_red")
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
    vault_path = APPDATA.joinpath("vault")
    if not vault_path.is_file() or force:
        core.make_vault(APPDATA, ctx.obj.get("password"))
        click.secho("A new vault has been created", fg="green")
    else:
        click.secho("A vault already exists", fg="red")


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
    if core.add_item(new_item, artifacts.decrypted, force):
        click.secho(f"Added new item: {name}", fg="green")
        encrypted: bytes = crypto.encrypt(
            artifacts.salt,
            ctx.obj.get("password"),
            artifacts.decrypted
        )
        core.dump_vault(APPDATA, encrypted)
    else:
        click.secho("Item already exists", fg="red")


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
    item: VaultRecord = core.get_item(name, artifacts.decrypted)
    if item is not None:
        for key, value in item.__dict__.items():
            click.secho(f"{key} -> ", nl=False, fg="yellow")
            click.echo(f"{value}")
    else:
        click.secho(f"Item not matched: {name}", fg="red")


@cli.command(help="Removes an item")
@click.argument("name")
@click.pass_context
def remove(ctx, name):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))
    if core.remove_item(name, artifacts.decrypted):
        click.echo(f"Item has been removed: {name}")
        encrypted: bytes = crypto.encrypt(
            artifacts.salt,
            ctx.obj.get("password"),
            artifacts.decrypted,
        )
        core.dump_vault(APPDATA, encrypted)
    else:
        click.secho(f"Item not matched: {name}", fg="red")


@cli.command(help="Returns all item names")
@click.pass_context
def list(ctx):
    artifacts: SetupFacts = setup(ctx.obj.get("password"))
    items: List = core.list_items(artifacts.decrypted)
    for item in items:
        click.secho(item, fg="yellow")


def setup(password) -> SetupFacts:
    salt: bytes = core.fetch_salt(APPDATA)
    vault: bytes = core.fetch_vault(APPDATA)
    try:
        decrypted: dict = crypto.decrypt(salt, password, vault)
    except IncorrectPassword as exc:
        exc.show()
        raise SystemExit(exc.exit_code)
    return SetupFacts(salt, vault, decrypted)


# TODO: Add 'env' command
# 'env' should list all user specified SHUSHI_ environment variables and
# link to documentation.
