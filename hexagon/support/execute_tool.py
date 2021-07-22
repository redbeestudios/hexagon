import importlib
import subprocess
import sys
import os
import traceback
from pathlib import Path
from typing import List, Union, Dict

from rich import traceback as rich_traceback

from hexagon.domain.tool import Tool
from hexagon.domain.env import Env
from hexagon.domain import configuration
from hexagon.support.printer import log

_command_by_file_extension = {"js": "node", "sh": "sh"}


def execute_action(tool: Tool, env_args, env: Env, args):
    action_to_execute: str = tool.action
    ext = action_to_execute.split(".")[-1]
    script_action_command = (
        _command_by_file_extension[ext] if ext in _command_by_file_extension else None
    )

    if script_action_command:
        _execute_script(
            script_action_command, action_to_execute, env_args or [], env, args
        )
    else:
        python_module_found = _execute_python_module(
            action_to_execute, tool, env, env_args, args
        )
        if python_module_found:
            return

        split_action = action_to_execute.split(" ")
        return_code, executed_command = _execute_command(
            split_action[0],
            env_args,
            args,
            action_args=split_action[1:],
        )

        if return_code != 0:
            log.error(f"{executed_command} returned code: {return_code}\n")

            if return_code == 127:
                log.error(f"Hexagon couldn't execute the action: [bold]{tool.action}")
                log.error("We tried:")
                log.error(
                    f"  - Your CLI's custom_tools_dir: [bold]{configuration.custom_tools_path}"
                )
                log.error(
                    "  - Hexagon repository of externals tools (hexagon.tools.external)"
                )
                log.error("  - A known script file (.js, .sh)")
                log.error("  - Running your action as a shell command directly")
            sys.exit(1)


def _execute_python_module(action_id: str, tool: Tool, env: Env, env_args, args):
    tool_action_module = _load_action_module(action_id) or _load_action_module(
        f"hexagon.tools.external.{action_id}"
    )

    if not tool_action_module:
        return False

    # noinspection PyBroadException
    try:
        tool_action_module.main(tool, env, env_args, args)
        return True
    except Exception:
        # log.error(f"Execution of tool [bold]{action_id}[/bold] thru:")
        __pretty_print_external_error(action_id)
        sys.exit(1)


def _execute_command(
    command: str, env_args, cli_args, env: Env = None, action_args: List[str] = None
):
    action_args = action_args if action_args else []
    hexagon_args = __sanitize_args_for_command(env_args, env, *cli_args)
    cmd_as_string = " ".join([command] + action_args + hexagon_args)

    return subprocess.call(cmd_as_string, shell=True), cmd_as_string


def _execute_script(command: str, script: str, env_args, env: Env, args):
    # Script should be relative to the project path
    script_path = os.path.join(configuration.project_path, script)
    if env and env.alias:
        del env.alias
    _execute_command(command, env_args, args, env, [script_path])


def __sanitize_args_for_command(*args: Union[List[any], Dict, Env]):
    positional = []
    named = []
    for arg in args:
        if isinstance(arg, (int, float, complex, str)):
            positional.append(str(arg))
        elif isinstance(arg, list):
            for a in arg:
                positional.append(str(a))
        elif not arg:
            continue
        else:
            try:
                named += [f"{k}={v}" for k, v in arg.items() if v]
            except AttributeError:
                # Unknown arg type, try to append it directly
                positional.append(f'"{str(arg)}"')
    return named + positional


def _load_action_module(action_id: str):
    try:
        return __load_module(action_id)
    except ModuleNotFoundError as e:
        if e.name == action_id:
            return None
        else:
            __pretty_print_external_error(action_id)
            log.error("Your custom action seems to have a module dependency error")
            sys.exit(1)


def __load_module(module: str):
    if module in sys.modules:
        return sys.modules[module]

    return importlib.import_module(module)


def __pretty_print_external_error(action_id):
    exc_type, exc_value, tb = sys.exc_info()

    trace = __find_python_module_in_traceback(action_id, tb)

    if trace:
        log.example(
            rich_traceback.Traceback.from_exception(
                exc_type,
                exc_value,
                trace,
            ),
            decorator_start=False,
            decorator_end=False,
        )
    else:
        log.error(exc_value)


def __find_python_module_in_traceback(action_id, tb):
    return next(
        (
            t
            for t, path, file_name in __walk_tb(tb)
            if file_name == action_id
            or path == os.path.join(configuration.custom_tools_path, action_id)
        ),
        None,
    )


def __walk_tb(tb):
    def extract_metadata(_t):
        try:
            p = Path(traceback.extract_tb(_t)[0].filename)
            return p.parent, p.stem
        except IndexError:
            return None

    while tb is not None:
        path, file_name = extract_metadata(tb)
        yield tb, path.__str__(), file_name
        tb = tb.tb_next
