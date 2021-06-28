from e2e.tests.utils.run import run_hexagon_e2e_test, write_to_process
from e2e.tests.utils.assertions import assert_process_ended, assert_process_output
from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER


def _shared_gui_assertions(process):
    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "Hi, which tool would you like to use today?",
            "┌──────────────────────────────────────────────────────────────────────────────",
            "",
            "",
            "",
            "⦾ Google",
            "",
            "ƒ Python Module Test",
            "",
            "ƒ Python Module Env Test",
            "",
            "ƒ Node Module Test",
            "",
            "ƒ Node Module Env Test",
            "",
            "⬡ Save Last Command",
            "",
            "⬡ Create A New Tool",
            "",
            "└──────────────────────────────────────────────────────────────────────────────",
            "",
        ],
    )


def test_execute_python_module_by_gui():
    process = run_hexagon_e2e_test(__file__)

    _shared_gui_assertions(process)

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}\n")

    assert_process_output(
        process,
        [
            ["Hi, which tool would you like to use today?", "ƒ Python Module Test"],
            "executed python module",
            "│",
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test python-module",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_by_argument():
    process = run_hexagon_e2e_test(__file__, ["python-module"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed python-module",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_by_alias():
    process = run_hexagon_e2e_test(__file__, ["pm"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed pm",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_env_and_arguments():
    process = run_hexagon_e2e_test(__file__, ["python-module", "env", "123", "abc"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed python-module in env with cli args:",
            "123",
            "abc",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_env_arguments():
    process = run_hexagon_e2e_test(__file__, ["python-module-env"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed python-module-env with env args:",
            "456",
            "def",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_node_module_by_gui():
    process = run_hexagon_e2e_test(__file__)

    _shared_gui_assertions(process)

    write_to_process(
        process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n"
    )

    assert_process_output(
        process,
        [
            ["Hi, which tool would you like to use today?", "ƒ Node Module Test"],
            "executed node module",
            "│",
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test node-module",
        ],
    )

    assert_process_ended(process)


def test_execute_node_module_by_argument():
    process = run_hexagon_e2e_test(__file__, ["node-module"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed node module",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_node_module_with_env_and_arguments():
    process = run_hexagon_e2e_test(__file__, ["node-module", "env", "arg1", "arg2"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed node module in env with args:",
            "arg1",
            "arg2",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_node_module_with_env_arguments():
    process = run_hexagon_e2e_test(__file__, ["node-module-env"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed node module in undefined with args:",
            "env_arg1",
            "env_arg2",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)
