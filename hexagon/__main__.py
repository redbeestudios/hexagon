import sys

from hexagon.domain import cli, tools, envs
from hexagon.plugins import collect_plugins
from hexagon.support.args import fill_args
from hexagon.support.execute.tool import select_and_execute_tool
from hexagon.support.help import print_help
from hexagon.support.hooks import HexagonHooks
from hexagon.support.printer import log
from hexagon.support.storage import (
    HexagonStorageKeys,
    store_user_data,
)
from hexagon.support.tracer import tracer
from hexagon.support.update.cli import check_for_cli_updates
from hexagon.support.update.hexagon import check_for_hexagon_updates


def main():
    _u, _tool, _env = fill_args(sys.argv, 3)

    if _tool == "-h" or _tool == "--help":
        return print_help(cli, tools, envs)

    collect_plugins()

    HexagonHooks.start.run()
    log.start(f"[bold]{cli.name}")
    log.gap()

    check_for_hexagon_updates()

    if cli.name == "Hexagon":
        log.info(
            _("msg.main.first_time_intro"), _("msg.main.first_time_tool"), gap_end=1
        )
    else:
        check_for_cli_updates()

    try:
        result = select_and_execute_tool(tools, _tool, _env, sys.argv[3:])

        log.gap()

        if result:
            for item in result:
                log.info(item)

        log.finish()

        command = tracer.command()
        if tracer.has_traced():
            log.extra(
                _("msg.main.tracer.run_again").format(
                    command=" ".join([cli.command, command])
                )
            )
            command_as_aliases = tracer.command_as_aliases(tools, envs)
            if command_as_aliases and command != command_as_aliases:
                log.extra(
                    _("msg.main.tracer.or").format(
                        command=" ".join([cli.command, command_as_aliases])
                    )
                )

        store_user_data(
            HexagonStorageKeys.last_command.value, f"{cli.command} {command}"
        )
    except KeyboardInterrupt:
        sys.exit(1)

    HexagonHooks.end.run()


if __name__ == "__main__":
    main()
