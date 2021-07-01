from typing import Any, Dict, List

from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator
from rich import print

from hexagon.cli.tracer import tracer


# Toda tool de hexagon tiene que tener un main que se va a invocar
# Los argumentos que se reciben son, en orden:
#   tool: La tool por la cual se ejecuto este modulo
#   env: El entorno indicado por el usuario
#   env_args: Los argumentos deifnidos para el entorno
#   cli_args: Otros argumentos que indico el usuario por CLI


def main(
    tool: Dict[str, Any],
    env: str = None,
    env_args: Any = None,
    cli_args: List[Any] = None,
):
    _name = cli_args[0] if cli_args and len(cli_args) > 0 else None

    # Es importante usar tracer.tracing para registrar los argumentos/sub_comandos que
    # se van ejecutando. de está manera hexagon puede recomendar al usuario
    # la manera de repetir el comando nuevamente sin prompts.
    name = tracer.tracing(
        _name
        or inquirer.text(
            message="¿Cómo es tu apellido?",
            validate=EmptyInputValidator("Poneme un apellido válido, por favor."),
        ).execute()
    )

    print("Tool.action:", tool["action"])
    print("Env:", env)
    print("Valor en tool.envs:", env_args)
    print("tu apellido es:", name)
