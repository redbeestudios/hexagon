from e2e.tests.utils.run import run_hexagon_e2e_test
from e2e.tests.utils.assertions import assert_process_ended, assert_process_output
from e2e.tests.utils.config import write_hexagon_config
from e2e.tests.utils.run import write_to_process
from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER
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
    process = run_hexagon_e2e_test(__file__, ["create-tool"])

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n")
    write_to_process(process, "a-new-action\n")
    write_to_process(process, "\r")
    write_to_process(process, "-command\n")
    write_to_process(process, "\n")
    write_to_process(process, f"{LONG_NAME}\n")
    write_to_process(process, f"{DESCRIPTION}\n")

    assert_process_ended(process)

    process = run_hexagon_e2e_test(
        __file__, ["a-new-action-command", "env", "my-last-name"]
    )

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "Tool.action: a-new-action",
            "Env: None",
            "Valor en tool.envs: None",
            "tu apellido es: my-last-name",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)
