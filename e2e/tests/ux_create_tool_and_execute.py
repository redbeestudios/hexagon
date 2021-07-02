from e2e.tests.utils.hexagon_spec import as_a_user
from e2e.tests.utils.config import write_hexagon_config
from e2e.tests.utils.path import e2e_test_folder_path

import os
import shutil

LONG_NAME = "Custom Action Test"
DESCRIPTION = "Hexagon Custom Action Test Description"

config_file = {
    "cli": {"name": "Test", "command": "hexagon-test", "custom_tools_dir": "."},
    "tools": {"google": {"long_name": "Google", "type": "web", "action": "open_link"}},
    "envs": {},
}


def _clear_custom_tool():
    custom_tool_path = os.path.join(e2e_test_folder_path(__file__), "a-new-action")
    if os.path.isdir(custom_tool_path):
        shutil.rmtree(custom_tool_path)


def test_creates_a_python_tool_and_executes_it():
    _clear_custom_tool()
    write_hexagon_config(__file__, config_file)

    (
        as_a_user(__file__)
        .run_hexagon(["create-tool"])
        .arrow_down()
        .arrow_down()
        .enter()
        .write("a-new-action\n")
        .write("\r")
        .write("-command\n")
        .enter()
        .write(f"{LONG_NAME}\n")
        .write(f"{DESCRIPTION}\n")
        .exit()
    )

    (
        as_a_user(__file__)
        .run_hexagon(["a-new-action-command", "env", "my-last-name"])
        .then_output_should_be(
            [
                "╭╼ Test",
                "│",
                "│ Tool.action: a-new-action",
                "│ Env: None",
                "│ Valor en tool.envs: None",
                "│ tu apellido es: my-last-name",
                "│",
                "╰╼",
            ]
        )
        .exit()
    )