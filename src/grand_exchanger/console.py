"""Module for high level console commands."""
import os
from typing import Any, Dict, List, Optional


import click


plugin_folder = os.path.join(os.path.dirname(__file__), "cli")


class CLI(click.MultiCommand):
    """CLI multi command class for loading command plugins."""

    def list_commands(self, ctx: click.Context) -> List[str]:
        """Lists all command groups from plugins in the plugin folder.

        Args:
            ctx (click.Context): A context object

        Returns:
            List[str]: A list of command group names.
        """
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and not filename.endswith("__init__.py"):
                rv.append(filename[:-3])

        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        """Returns a command object for a command group name.

        Args:
            ctx (click.Context): A context object
            name (str): A valid command group name.

        Returns:
            Optional[click.Command]: The command object.__class__(
        """
        ns: Dict[str, Any] = {}
        fn = os.path.join(plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)

        return ns["cli"]


@click.command(cls=CLI)
def cli() -> None:
    """CLI group."""
    pass
