from typing import Any, Dict, List


def main(
    action: Dict[str, Any],
    env: str = None,
    env_args: Any = None,
    cli_args: List[Any] = [],
):
    to_print = f"executed {action['action']}"

    if env:
        to_print += f" in {env}"

    print(to_print)

    if env_args:
        print("Env args:")
        print(env_args)

    if cli_args and len(cli_args) > 0:
        print("Cli args:")
        for cli_arg in cli_args:
            print(cli_arg)
