import sys
from hexagon.cli.args import fill_args


def main(_):
    _, _tool, _env, _arg1, _arg2 = fill_args(sys.argv, 5)
    to_print = "executed"

    if _tool:
        to_print += f" {_tool}"
    else:
        to_print += " python module"

    if _env:
        to_print += f" in {_env}"

    if _arg1 and _arg2:
        to_print += " with cli args:"
        print(to_print)
        print(_arg1)
        print(_arg2)
    else:
        print(to_print)
