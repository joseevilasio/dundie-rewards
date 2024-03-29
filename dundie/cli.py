import pkg_resources
import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core
from dundie.utils.export import export_csv
from dundie.utils.login import handles_query_for_user, require_password

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(pkg_resources.get_distribution("dundie").version)
def main():
    """Dunder Mifflin Rewards System.

    This cli application controls Dunder Mifflin rewards.

    - admins can load information tot he people database and assign points.
    - users can view reports and transfer points.

    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
def load(filepath):
    """Loads the file to the database.

    ## Features

    - Validates data
    - Parses the file
    - Loads to database
    """

    if require_password(admin_only=True):
        table = Table(title="Dunder Mifflin Associates")
        headers = ["email", "name", "dept", "role", "currency", "created"]
        for header in headers:
            table.add_column(header, style="magenta")

        result = core.load(filepath)
        for person in result:
            table.add_row(*[str(value) for value in person.values()])

        console = Console()
        console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Shows information about user or dept."""

    if require_password(admin_only=False):
        result = handles_query_for_user(core.read, **query)

        if output:
            export_csv(output=output, result=result)
            console = Console()  # pragma: no cover
            console.print(
                f"Sucess! File saved in {output} ",
                justify="center",
                style="red on white",
            )  # pragma: no cover

        elif len(result) == 0:
            # TODO: Interface in command line make too pretty
            console = Console()
            console.print(
                "Nothing to show", justify="center", style="red on white"
            )

        else:
            table = Table(title="Dunder Mifflin Report")
            for key in result[0]:
                table.add_column(
                    key.title().replace("_", " "), style="magenta"
                )

            for person in result:
                person["value"] = f"{person['value']:.2f}"
                person["balance"] = f"{person['balance']:.2f}"
                table.add_row(*[str(value) for value in person.values()])

            console = Console()
            console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context
def add(ctx, value, **query):
    """Add points to the user or dept."""

    if require_password(admin_only=True):
        core.add(value, **query)
        ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.pass_context
def remove(ctx, value, **query):
    """Removes points from the user or dept."""

    if require_password(admin_only=True):
        core.add(-value, **query)
        ctx.invoke(show, **query)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
def movements(**query):
    """Show moviments points from the user or dept."""

    if require_password(admin_only=False):
        result = handles_query_for_user(core.read_movements, **query)

        if len(result) == 0:
            console = Console()
            console.print(
                "Nothing to show", justify="center", style="red on white"
            )

        else:
            table = Table(title="Dunder Mifflin Report", style="red")

            for key in result[0]:
                table.add_column(key.title().replace("_", " "), style="green")

            for person in result:
                person["value"] = f"{person['value']:.2f}"
                table.add_row(*[str(value) for value in person.values()])

            console = Console()
            console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.argument("to", type=click.STRING, required=True)
@click.pass_context
def transfer(ctx, value, to):
    """Transfer points between users."""

    if require_password(admin_only=False):
        core.transfer(value, to)
        ctx.invoke(show)
