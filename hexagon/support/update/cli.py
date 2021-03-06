import os
import re
import sys

from InquirerPy import inquirer

from hexagon.domain import cli, configuration
from hexagon.support.cli.command import (
    execute_command_in_cli_project_path,
    output_from_command_in_cli_project_path,
)
from hexagon.support.cli.git import load_cli_git_config
from hexagon.support.dependencies import scan_and_install_dependencies
from hexagon.support.printer import log
from hexagon.support.update.shared import already_checked_for_updates


def check_for_cli_updates():
    if os.getenv("HEXAGON_CLI_UPDATE_DISABLED"):
        return
    if already_checked_for_updates():
        return

    cli_git_config = load_cli_git_config()
    if not cli_git_config:
        return

    current_git_branch_status = output_from_command_in_cli_project_path("git status")
    current_git_branch = re.search(r"On branch (.+)", current_git_branch_status).groups(
        0
    )[0]

    not_in_head_branch = current_git_branch != cli_git_config.head_branch

    if not_in_head_branch:
        try:
            execute_command_in_cli_project_path(
                f"git checkout {cli_git_config.head_branch}"
            )
        except Exception:
            return

    execute_command_in_cli_project_path("git remote update")

    branch_status = output_from_command_in_cli_project_path("git status -uno")

    if "is behind" in branch_status:
        log.info(
            _("msg.support.update.cli.new_version_available").format(cli_name=cli.name)
        )
        if not inquirer.confirm(
            _("action.support.update.cli.confirm_update"), default=True
        ).execute():
            return
        execute_command_in_cli_project_path("git pull", show_stdout=True)
        scan_and_install_dependencies(configuration.custom_tools_path)
        log.info(_("msg.support.update.cli.updated"))
        log.finish()
        sys.exit(1)

    if not_in_head_branch:
        execute_command_in_cli_project_path(f"git checkout {current_git_branch}")
