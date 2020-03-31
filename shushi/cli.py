import os
from typing import List

import click

from . import core, crypto
from .constants import APPDATA
from .record import VaultRecord


@click.group()
@click.option("-p", "--password", default=None, help="Vault password")
@click.pass_context
def cli(ctx, password):
    ctx.ensure_object(dict)
    password_ = password or os.environ.get("SHUSHI_PASSWORD", None)
    if password_ is not None:
        ctx.obj["password"] = password_
        ctx.obj["salt"] = core.fetch_salt(APPDATA)
        ctx.obj["vault"] = core.fetch_vault(APPDATA)
        ctx.obj["decrypted"] = crypto.decrypt(
            ctx.obj.get("salt"),
            ctx.obj.get("password"),
            ctx.obj.get("vault")
        )
    else:
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
def make(password, force):
    vault_path = APPDATA.joinpath("vault")
    if not vault_path.is_file() or force:
        core.make_vault(APPDATA, password)
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
    new_item: dict = item_builder(name)
    if core.add_item(new_item, ctx.obj.get("decrypted"), force):
        click.secho(f"Added new item: {name}", fg="green")
        encrypted: bytes = crypto.encrypt(
            ctx.obj.get("salt"),
            ctx.obj.get("password"),
            ctx.obj.get("decrypted")
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
    item: VaultRecord = core.get_item(name, ctx.obj.get("decrypted"))
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
    if core.remove_item(name, ctx.obj.get("decrypted")):
        click.echo(f"Item has been removed: {name}")
        encrypted: bytes = crypto.encrypt(
            ctx.obj.get("salt"),
            ctx.obj.get("password"),
            ctx.obj.get("decrypted")
        )
        core.dump_vault(APPDATA, encrypted)
    else:
        click.secho(f"Item not matched: {name}", fg="red")


@cli.command(help="Returns all item names")
@click.pass_context
def list(ctx):
    items: List = core.list_items(ctx.obj.get("decrypted"))
    for item in items:
        click.secho(item, fg="yellow")

# TODO: Add 'env' command
# 'env' should list all user specified SHUSHI_ environment variables and
# link to documentation.
