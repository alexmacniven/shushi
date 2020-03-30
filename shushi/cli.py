import click
from . import core
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
