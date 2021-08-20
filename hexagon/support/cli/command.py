import subprocess
from hexagon.domain import configuration


def output_from_command_in_cli_project_path(command: str) -> str:
    return subprocess.check_output(
        command,
        shell=True,
        cwd=configuration.project_path,
        text=True,
        stderr=subprocess.DEVNULL,
    )


def execute_command_in_cli_project_path(command: str) -> None:
    assert (
        subprocess.check_call(
            command,
            shell=True,
            cwd=configuration.project_path,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        == 0
    )
