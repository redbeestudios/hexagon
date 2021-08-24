from typing import Any, Dict, List

from pydantic.error_wrappers import ValidationError
from .update import (
    UpdateOptions,
    update_options_keys,
    default_update_options,
)
from pydantic import BaseModel
import os
import sys
from hexagon.support.printer import log


class Options(BaseModel):
    update: UpdateOptions


OptionsKeysMapLeaf = Dict[str, str]
OptionsKeysMapBranch = Dict[str, OptionsKeysMapLeaf]
OptionsKeysMap = Dict[str, OptionsKeysMapBranch or OptionsKeysMapLeaf]

options_keys_map: OptionsKeysMap = {"update": update_options_keys}
defaults = {"update": default_update_options}
options = None


def _flatten_option_leafs_with_dot_notation(options_keys_map: OptionsKeysMap):
    leafs: List[str] = []
    for key, value in options_keys_map.items():
        if isinstance(value, list):
            for val in value:
                leafs.append(f"{key}.{val}")
        elif isinstance(value, dict):
            leafs.extend(_flatten_option_leafs_with_dot_notation(value))
    return leafs


def _get_first_and_other_keys_from_dot_notation(key: str or List[str]):
    if isinstance(key, str):
        key = key.split(".")
    return key[0] if len(key) > 0 else None, key[1:]


def _access_dict_with_dot_notation(dictionary: Dict[str, Any], key: str):
    first_key, other_keys = _get_first_and_other_keys_from_dot_notation(key)

    if first_key not in dictionary:
        return None
    next_value = dictionary[first_key]
    if len(other_keys) == 0:
        return next_value
    else:
        return _access_dict_with_dot_notation(next_value, other_keys)


def _write_dict_with_dot_notation(dictionary: Dict[str, Any], key: str, value: Any):
    first_key, other_keys = _get_first_and_other_keys_from_dot_notation(key)

    if len(other_keys) == 0:
        dictionary[first_key] = value
    else:
        if first_key not in dictionary:
            dictionary[first_key] = {}
        _write_dict_with_dot_notation(dictionary[first_key], other_keys, value)


def load_hexagon_options(
    cli_options: Dict[str, str], local_options: Dict[str, Any]
) -> Options:
    global options
    flattened_keys = _flatten_option_leafs_with_dot_notation(options_keys_map)
    opt = {}

    for key in flattened_keys:
        candidate = cli_options[key] if key in cli_options else None

        if not candidate:
            candidate = os.getenv("HEXAGON_" + key.replace(".", "_").upper())
        if not candidate and local_options:
            candidate = _access_dict_with_dot_notation(local_options, key)
        if not candidate:
            first_key, _ = _get_first_and_other_keys_from_dot_notation(key)
            candidate = defaults[first_key] if first_key in defaults else None
            if candidate:
                opt[first_key] = candidate
                continue

        _write_dict_with_dot_notation(opt, key, candidate)

    try:
        options = Options(**opt)
    except ValidationError as errors:
        log.error(str(errors))
        sys.exit(1)


def get_hexagon_options():
    global options
    return options
