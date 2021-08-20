from hexagon.support.cli.git import load_cli_git_config
from hexagon.support.cli.command import (
    execute_command_in_cli_project_path,
    output_from_command_in_cli_project_path,
)
from hexagon.support.printer import log
from hexagon.support.update.shared import already_checked_for_updates
import os
import re
from hexagon.domain import cli
from InquirerPy import inquirer
from halo import Halo
import sys


def check_for_cli_updates():
    if os.getenv("HEXAGON_CLI_UPDATE_DISABLED"):
        return
    if already_checked_for_updates():
        return

    current_git_branch_status = output_from_command_in_cli_project_path("git status")
    current_git_branch = re.search(r"On branch (.+)", current_git_branch_status).groups(
        0
    )[0]

    cli_git_config = load_cli_git_config()
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
        log.info(f"New [cyan]{cli.name} [white]version available")
        if not inquirer.confirm("Would you like to update?", default=True).execute():
            return
        # TODO: Use helper to show spinner control
        with Halo(text=f"Updating {cli.name}"):
            execute_command_in_cli_project_path("git pull")
        log.info("[green]🗸 [white]Updated to latest version")
        log.finish()
        sys.exit(1)

    if not_in_head_branch:
        execute_command_in_cli_project_path(f"git checkout {current_git_branch}")
