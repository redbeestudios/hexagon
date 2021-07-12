from pydantic import ValidationError
from rich.syntax import Syntax

from hexagon.support.printer import log


def display_yaml_errors(errors: ValidationError, ruamel_yaml, yaml_path):
    yml = open(yaml_path, "r").read()
    errors_as_dict = errors.errors()
    log.error(f"There were {len(errors_as_dict)} error(s) in your YAML")
    for err in errors_as_dict:
        (start, line_number, end) = __lines_of_error(err, ruamel_yaml)
        log.error(f"\n✗ [bold]{'.'.join(err['loc'])}[/bold] -> {err['msg']}")
        log.example(
            Syntax(
                "\n".join(yml.splitlines()[start:end]),
                "yaml",
                line_numbers=True,
                start_line=start + 1,
            ),
            decorator_start=False,
            decorator_end=False,
        )


def __lines_of_error(err, ruamel_yaml):
    line_number = __yaml_line_number(ruamel_yaml, err["loc"])
    return line_number - (2 if line_number > 1 else 1), line_number, line_number + 4


def __yaml_line_number(yml, loc):
    if len(loc) == 1:
        try:
            return yml[loc[0]].lc.line
        except (LookupError, TypeError):
            return yml.lc.line
    else:
        return __yaml_line_number(yml[loc[0]], loc[1:])
