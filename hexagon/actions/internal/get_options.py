from datetime import timedelta
from typing import Any, Dict
from hexagon.domain import get_options
from hexagon.support.printer import log


def _print_dict_indented(dictionary: Dict[str, Any], indent_level=0):
    for key, value in dictionary.items():
        if isinstance(value, (str, int, float, timedelta)):
            log.info(" " * indent_level * 2 + f"{key}: {value}")
        else:
            log.info(key)
            _print_dict_indented(value.__dict__, indent_level + 1)


def main(*_):
    _print_dict_indented(get_options().__dict__)
