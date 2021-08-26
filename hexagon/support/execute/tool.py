from hexagon.support.yaml import display_yaml_errors
from prompt_toolkit.validation import ValidationError
from hexagon.support.execute.action import execute_action
from hexagon.support.wax import search_by_name_or_alias, select_env, select_tool
from hexagon.domain.tool import (
    GroupTool,
    Tool,
    ToolGroupConfigFile,
)
from typing import List
from hexagon.domain import envs, configuration
from hexagon.support.tracer import tracer
from hexagon.domain.configuration import (
    read_configuration_file,
    register_custom_tools_path,
)
from hexagon.support.printer import log
import sys
import os


def select_and_execute_tool(
    tools: List[Tool],
    tool_argument: str = None,
    env_argument: str = None,
    arguments: List[object] = None,
    custom_tools_path=None,
) -> List[str]:
    arguments = arguments if arguments else []
    tool = search_by_name_or_alias(tools, tool_argument)
    env = search_by_name_or_alias(envs, env_argument)

    tool = select_tool(tools, tool)
    tracer.tracing(tool.name)

    env, params = select_env(envs, tool.envs, env)
    if env:
        tracer.tracing(env.name)

    if isinstance(tool, GroupTool):
        return _execute_group_tool(tool, env_argument, arguments, custom_tools_path)

    result = execute_action(tool, params, env, arguments, custom_tools_path)
    return result


def _execute_group_tool(
    tool: Tool,
    env_argument: str = None,
    arguments: List[object] = None,
    previous_custom_tools_path: str = None,
) -> List[str]:
    config_file_path = os.path.join(configuration.project_path, tool.tools)

    try:
        group_config_yaml = read_configuration_file(config_file_path)
    except FileNotFoundError:
        log.error(f"File {config_file_path} could not be found")
        sys.exit(1)

    try:
        group_config = ToolGroupConfigFile(**group_config_yaml)
    except ValidationError as errors:
        display_yaml_errors(errors, group_config_yaml, config_file_path)
        sys.exit(1)

    # Shift cli args one place to the right
    tool_argument = env_argument
    env_argument = arguments[0] if len(arguments) > 0 else None
    sub_tool_arguments = arguments[1:]

    custom_tools_absolute_path = register_custom_tools_path(
        group_config.custom_tools_dir if group_config.custom_tools_dir else ".",
        os.path.dirname(tool.tools),
    )

    return select_and_execute_tool(
        group_config.tools,
        tool_argument,
        env_argument,
        sub_tool_arguments,
        custom_tools_absolute_path
        if custom_tools_absolute_path
        else previous_custom_tools_path,
    )
