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
            "ƒ Python Module Asterisk Env Test",
            "",
            "ƒ Node Module Test",
            "",
            "ƒ Node Module Env Test",
            "",
            "⬡ Save Last Command",
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
            "executed python-module",
            "│",
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test python-module",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_env_by_gui():
    process = run_hexagon_e2e_test(__file__)

    _shared_gui_assertions(process)

    write_to_process(process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n")

    assert_process_output(
        process,
        [
            ["Hi, which tool would you like to use today?", "ƒ Python Module Env Test"],
        ],
    )

    assert_process_output(
        process, ["On which environment?", "", "", "", "", "dev", "", "qa", "", "", ""]
    )

    write_to_process(process, "\n")

    assert_process_output(
        process,
        [
            ["On which environment?", "dev"],
            "executed python-module in dev",
            "Env args:",
            "[789, 'ghi']",
            "│",
            "╰╼",
            "Para repetir este comando:",
            "    hexagon-test python-module",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_env_asterisk_by_gui():
    process = run_hexagon_e2e_test(__file__)

    _shared_gui_assertions(process)

    write_to_process(
        process, f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n"
    )

    assert_process_output(
        process,
        [
            [
                "Hi, which tool would you like to use today?",
                "ƒ Python Module Asterisk Env Test",
            ],
            "",
            "executed python-module",
            "Env args:",
            "all_envs",
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
            "executed python-module",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_env_and_arguments():
    process = run_hexagon_e2e_test(__file__, ["python-module-env", "dev", "123", "abc"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed python-module in dev",
            "Env args:",
            "[789, 'ghi']",
            "Cli args:",
            "123",
            "abc",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_python_module_with_other_env():
    process = run_hexagon_e2e_test(__file__, ["python-module-env", "qa"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed python-module in qa",
            "Env args:",
            "ordereddict([('foo', 'foo'), ('bar', 'bar')])",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_script_module_by_gui():
    process = run_hexagon_e2e_test(__file__)

    _shared_gui_assertions(process)

    write_to_process(
        process,
        f"{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}{ARROW_DOWN_CHARACTER}\n",
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


def test_execute_script_module_by_argument():
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


def test_execute_script_module_with_env_and_arguments():
    process = run_hexagon_e2e_test(__file__, ["node-module-env", "dev", "arg1", "arg2"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed node module",
            "CLI arguments:",
            "env=dev",
            "789",
            "ghi",
            "arg1",
            "arg2",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)


def test_execute_script_module_with_other_env():
    process = run_hexagon_e2e_test(__file__, ["node-module-env", "qa"])

    assert_process_output(
        process,
        [
            "╭╼ Test",
            "│",
            "executed node module",
            "CLI arguments:",
            "foo=foo",
            "bar=bar",
            "env=qa",
            "│",
            "╰╼",
        ],
    )

    assert_process_ended(process)
