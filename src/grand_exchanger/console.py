import os
from typing import Any, Dict, List, Optional


import click


plugin_folder = os.path.join(os.path.dirname(__file__), "cli")


class CLI(click.MultiCommand):
    def list_commands(self, ctx: click.Context) -> List[str]:
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith(".py") and not filename.endswith("__init__.py"):
                rv.append(filename[:-3])

        rv.sort()
        return rv

    def get_command(self, ctx: click.Context, name: str) -> Optional[click.Command]:
        ns: Dict[str, Any] = {}
        fn = os.path.join(plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)

        return ns["cli"]


@click.command(cls=CLI)
def cli() -> None:
    pass
