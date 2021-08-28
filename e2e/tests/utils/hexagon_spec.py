import time
from typing import Callable, Dict, List, Optional

from e2e.tests.utils.assertions import (
    Expected_Process_Output,
    assert_process_output,
    assert_process_ended,
)
from e2e.tests.utils.cli import ARROW_DOWN_CHARACTER
from e2e.tests.utils.config import write_hexagon_config
from e2e.tests.utils.run import (
    run_hexagon_e2e_test,
    write_to_process,
    clean_hexagon_environment,
)


class HexagonSpec:
    def __init__(self, file) -> None:
        self.__file = file
        self.process = None
        self.command = None

    def given_a_cli_yaml(self, config: dict):
        write_hexagon_config(self.__file, config)
        return self

    def run_hexagon(
        self,
        command: List[str] = None,
        os_env_vars: Optional[Dict[str, str]] = None,
        test_file_path_is_absoulte: bool = False,
    ):
        __tracebackhide__ = True
        if command:
            self.command = command
            self.process = run_hexagon_e2e_test(
                self.__file,
                self.command,
                os_env_vars=os_env_vars,
                test_file_path_is_absoulte=test_file_path_is_absoulte,
            )
        else:
            self.process = run_hexagon_e2e_test(
                self.__file,
                os_env_vars=os_env_vars,
                test_file_path_is_absoulte=test_file_path_is_absoulte,
            )
        return self

    def with_shared_behavior(self, func: Callable):
        __tracebackhide__ = True
        func(self)
        return self

    def then_output_should_be(
        self,
        expected_output: List[Expected_Process_Output],
        discard_until_initial=False,
    ):
        __tracebackhide__ = True
        assert_process_output(
            self.process, expected_output, discard_until_initial=discard_until_initial
        )
        return self

    def arrow_down(self):
        __tracebackhide__ = True
        write_to_process(self.process, ARROW_DOWN_CHARACTER)
        return self

    def enter(self):
        __tracebackhide__ = True
        return self.write("\n")

    def carriage_return(self):
        __tracebackhide__ = True
        return self.write("\r")

    def input(self, text: str):
        __tracebackhide__ = True
        return self.write(f"{text}\n")

    def write(self, text: str):
        __tracebackhide__ = True
        write_to_process(self.process, text)
        return self

    def exit(self, status: int = 0):
        __tracebackhide__ = True
        assert_process_ended(self.process, status)
        clean_hexagon_environment()

    @property
    def _and_(self):
        return self

    def force_exit(self):
        return self.write("^C")

    def wait(self, seconds: int):
        time.sleep(seconds)
        return self


def as_a_user(test_file):
    return HexagonSpec(test_file)
