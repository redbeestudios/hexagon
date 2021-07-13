from itertools import groupby
from typing import List

from hexagon.domain.env import Env
from hexagon.domain.tool import Tool
from hexagon.domain.cli import Cli
from hexagon.support.printer import log


# TODO: add e2e tests of help
def print_help(cli_config: Cli, tools: List[Tool], envs: List[Env]):
    """
    Print the command line help text based on the tools and envs in configuration yaml

    :param cli_config:
    :param tools:
    :param envs:
    :return:
    """
    if cli_config.name == "Hexagon":
        log.info("[bold]Hexagon", gap_end=1)
        log.info("You are executing Hexagon without an install.")
        log.info('To get started run hexagon\'s "Install Hexagon" tool')
        return

    log.info(f"[bold]{cli_config.name}", gap_end=1)

    log.info("[bold][u]Envs:")
    for env in envs:
        log.info(f'  {env.name + (" (" + env.alias + ")" if env.alias else "")}')

    log.info("[bold][u]Tools:", gap_start=2)

    data = sorted(tools, key=lambda t: t.type, reverse=True)

    for gk, g in groupby(data, lambda t: t.type):
        log.info(f"[bold]{gk}:", gap_start=1)

        for tool in g:
            log.info(
                f'  {tool.name + (" (" + tool.alias + ")" if tool.alias else ""):<60}[dim]{tool.long_name or ""}'
            )
            if tool.description:
                log.info(f'  {"": <60}[dim]{tool.description}', gap_end=1)
